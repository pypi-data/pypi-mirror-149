import json
import logging
from datetime import date
from itertools import chain
from json import JSONDecodeError

from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.db.models import (
    DateField,
    FloatField,
    ForeignKey,
    ForeignObjectRel,
    IntegerField,
    Manager,
    Model,
    Q,
)
from django.db.models.constants import LOOKUP_SEP
from django.shortcuts import redirect
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _
from django.views import View

from pfx.pfxcore.decorator import rest_api
from pfx.pfxcore.exceptions import (
    APIError,
    ForbiddenError,
    JsonErrorAPIError,
    NotFoundError,
    UnauthorizedError,
)
from pfx.pfxcore.fields import MediaField, MinutesDurationField
from pfx.pfxcore.http import JsonResponse
from pfx.pfxcore.model_resolver import (
    MetaResolver,
    ObjectResolver,
    PropertyField,
    VirtualField,
)
from pfx.pfxcore.models import JSONReprMixin
from pfx.pfxcore.shortcuts import f, get_object, parse_bool
from pfx.pfxcore.storage.s3_storage import StorageException

logger = logging.getLogger(__name__)

LIST_META = ['count', 'pagination']


# HTTP 404 handler
def resource_not_found(request, exception):
    return NotFoundError().response


class ModelMixin():
    queryset = None
    fields = []
    readonly_fields = []

    def get_object(self, **kwargs):
        return get_object(self.get_queryset(), **kwargs)

    def get_queryset(self):
        return self.queryset

    def get_list_queryset(self):
        return self.get_queryset()

    def get_fields(self):
        return self.fields or [f.name for f in self.model._meta.fields]

    def get_model_fields(self):
        for fdescr in self.get_fields():
            fname = isinstance(fdescr, tuple) and fdescr[0] or fdescr
            yield fname, MetaResolver(self.model).get_field(fdescr)

    @property
    def _auto_readonly_fields(self):
        # Related fields and property fields are always readonly.
        for fname, field in self.get_model_fields():
            if (LOOKUP_SEP in fname or isinstance(field, PropertyField) or
                    isinstance(field, VirtualField)):
                yield fname

    def get_readonly_fields(self, obj=None):
        return chain(self._auto_readonly_fields, self.readonly_fields)

    @property
    def model(self):
        return self.get_queryset().model

    @property
    def model_name(self):
        return self.model._meta.verbose_name

    @property
    def date_format(self):
        return parse_bool(self.request.GET.get('date_format'))

    def _json_object(self, obj):
        if isinstance(obj, JSONReprMixin):
            return obj.json_repr()
        return dict(pk=obj.pk, resource_name=str(obj))

    def message_response(self, message, **kwargs):
        return JsonResponse(dict(message=message, **kwargs))


class ModelResponseMixin(ModelMixin):
    def serialize_field(self, obj, field_descr):
        value = ObjectResolver(obj).get_value(field_descr)
        field = MetaResolver(self.model).get_field(field_descr)
        if self.date_format and isinstance(value, date):
            return dict(
                value=value,
                formatted=date_format(
                    value, format='SHORT_DATE_FORMAT', use_l10n=True))
        if isinstance(field, MinutesDurationField) or (
                isinstance(field, (PropertyField, VirtualField)) and
                field.internal_type == 'MinutesDurationField'):
            return MinutesDurationField.to_json(value)
        if isinstance(value, Model):
            return self._json_object(value)
        if isinstance(value, Manager):
            return [self._json_object(o) for o in value.all()]
        if hasattr(field, 'choices') and field.choices:
            choices = {k: v for k, v in field.choices}
            if value in choices:
                return dict(value=value, label=_(choices[value]))
            else:  # pragma: no cover
                return None
        return value

    def serialize_object(self, obj, **fields):
        vals = self._json_object(obj)
        vals.update(fields)
        return vals

    def response(self, o, **meta):
        def _name(fd):
            return isinstance(fd, tuple) and fd[0] or fd

        return JsonResponse(self.serialize_object(o, **{
            _name(f): self.serialize_field(o, f)
            for f in self.get_fields()}, meta=meta))

    def validate(self, resolver, created=False, **kwargs):
        resolver.validate(**kwargs)

    def is_valid(self, resolver, created=False):
        resolver.save()
        message = (
                created and
                _("{model} {obj} created.") or
                _("{model} {obj} updated."))
        object = self.get_object(pk=resolver.object.pk)
        return self.response(
            object, message=f(
                message, model=self.model_name, obj=object))

    def is_invalid(self, resolver, errors):
        return JsonResponse(errors, status=422)

    def field_meta(self, field):
        name = field.name
        if hasattr(field, 'verbose_name'):
            name = field.verbose_name
        elif hasattr(field, 'related_model'):
            if (hasattr(field, 'multiple') and field.multiple and
                    hasattr(field.related_model._meta, 'verbose_name_plural')):
                name = field.related_model._meta.verbose_name_plural
            elif hasattr(
                field.related_model._meta, 'verbose_name'
            ):  # pragma: no cover
                name = field.related_model._meta.verbose_name
        if isinstance(field, MinutesDurationField):
            res = {'type': 'MinutesDurationField', 'name': name}
        else:
            res = {'type': field.get_internal_type(), 'name': name}
        if hasattr(field, 'choices') and field.choices:
            res['choices'] = [
                dict(label=_(v), value=k) for k, v in field.choices]
        res['readonly'] = field.name in self.get_readonly_fields()
        if not res['readonly']:
            res['required'] = not (
                getattr(field, 'null', False) or
                getattr(field, 'blank', False))
        return res

    def object_meta(self):
        return {n: self.field_meta(f) for n, f in self.get_model_fields()}

    @rest_api("/meta", method="get")
    def get_meta(self, *args, **kwargs):
        return JsonResponse(self.object_meta())


class BodyMixin:
    def deserialize_body(self):
        try:
            return json.loads(self.request.body)
        except JSONDecodeError as e:
            raise JsonErrorAPIError(e)


class ModelBodyMixin(BodyMixin, ModelMixin):
    def _field_data(self, field_name, value):
        field = MetaResolver(self.model).get_field(field_name)
        if isinstance(field, ForeignObjectRel):  # pragma: no cover
            raise Exception(
                f"{'.'.join([self.__module__, self.__class__.__name__])}: "
                "Reverse related fields are not editable, "
                f"add '{field_name}' in readonly_fields.")
        if isinstance(field, ForeignKey):
            pk = (value['pk'] if isinstance(value, dict) and 'pk' in value
                  else value)
            return f'{field_name}_id', pk or None
        if hasattr(field, 'choices') and field.choices:
            value = (value['value']
                     if isinstance(value, dict) and 'value' in value
                     else value)
        elif isinstance(field, DateField):
            value = (value['value']
                     if isinstance(value, dict) and 'value' in value
                     else value)
        elif isinstance(field, IntegerField):
            value = value if value != '' else None
        elif isinstance(field, FloatField):
            value = value if value != '' else None
        elif isinstance(field, MinutesDurationField):
            value = (value['human_format'] if isinstance(value, dict) and
                     'human_format' in value
                     else value != '' and value or None)
        return field_name, value

    def get_model_data(self, obj, data, created):
        data.pop('id', None)
        data.pop('pk', None)
        ro_fields = list(self.get_readonly_fields(obj))
        return dict(
            self._field_data(k, v) for k, v in data.items()
            # Todo: throw an error for non existing fields.
            if k in self.get_fields() and
            # Todo: Log a warning for readonly ignores fields.
            k not in ro_fields and
            # Deny API changes on technical django _id and _pk fields.
            k[-3:] not in ('_id', '_pk'))


class ListRestViewMixin(ModelResponseMixin):
    list_fields = []
    filters = []

    def get_list_fields(self):
        return self.list_fields or self.get_fields()

    def parse_list_meta(self):
        meta_arg = self.request.GET.get('meta', 'all')
        meta = meta_arg.split(',') or []
        if 'all' in meta:
            return LIST_META
        return meta

    def _list_meta_count(self):
        return self.get_list_queryset().count()

    def _list_meta_pagination(self):
        return dict(
            page_size=int(self.request.GET.get('page_size', 10)),
            page=int(self.request.GET.get('page', 1)),
            page_subset=int(self.request.GET.get('page_subset', 5)))

    def _list_meta_subset(self):
        return dict(
            limit=int(self.request.GET.get('limit', 10)),
            offset=int(self.request.GET.get('offset', 0)))

    def build_list_meta(self):
        def _meta(meta):
            fn = getattr(self, f'_list_meta_{meta}', None)
            if not callable(fn):
                raise APIError(
                    _("Meta {meta} does not exists.").format(meta=meta))
            return fn

        return {
            meta: _meta(meta)()
            for meta in self.parse_list_meta()}

    def search_filter(self, search):  # pragma: no cover
        return Q()

    @rest_api("/filters", method="get")
    def get_filter(self, *args, **kwargs):
        return JsonResponse({
            'items': [f.meta for f in self.filters]})

    def get_list_queryset(self):
        qs = super().get_list_queryset()
        search = self.request.GET.get('search')
        for filter in self.filters:
            qs = qs.filter(filter.query(self.request.GET))
        if search:
            qs = qs.filter(
                self.search_filter(search))
        order = self.request.GET.get('order')
        if order:
            qs = qs.order_by(*order.split(','))
        return qs

    def get_list_result(self, qs):
        def _name(fd):
            return isinstance(fd, tuple) and fd[0] or fd

        for o in qs:
            yield self.serialize_object(o, **{
                _name(f): self.serialize_field(o, f)
                for f in self.get_list_fields()})

    @rest_api("", method="get")
    def get_list(self, *args, **kwargs):
        res = {}
        meta = self.build_list_meta()
        qs = self.get_list_queryset()
        if 'pagination' in meta:
            count = qs.count()
            pagination = meta['pagination']
            page = pagination['page']
            limit = pagination['page_size']
            page_count = (1 + (count - 1) // limit) or 1
            offset = (page - 1) * limit
            subset = pagination['page_subset']
            subset_first = min(
                max(page - subset // 2, 1), max(page_count - subset + 1, 1))
            qs = qs.all()[offset:offset + limit]
            pagination.update(dict(
                count=count,
                page_count=page_count,
                subset=list(range(
                    subset_first,
                    min(subset_first + subset, page_count + 1)))))
        elif 'subset' in meta:
            count = qs.count()
            subset = meta['subset']
            limit = subset['limit']
            page_count = (1 + (count - 1) // limit) or 1
            offset = subset['offset']
            qs = qs.all()[offset:offset + limit]
            subset.update(dict(
                count=count,
                page_count=page_count,
                limit=limit,
                offset=offset))
        else:
            qs = qs.all()
        if meta:
            res['meta'] = meta
        res['items'] = list(self.get_list_result(qs))
        return JsonResponse(res)


class DetailRestViewMixin(ModelResponseMixin):

    @rest_api("/<int:id>", method="get")
    def get(self, id, *args, **kwargs):
        obj = self.get_object(pk=id)
        return self.response(obj)


class SlugDetailRestViewMixin(ModelResponseMixin):
    SLUG_FIELD = "slug"

    @rest_api("/slug/<slug:slug>", method="get")
    def get_by_slug(self, slug, *args, **kwargs):
        obj = self.get_object(**{self.SLUG_FIELD: slug})
        return self.response(obj)


class CreateRestViewMixin(ModelBodyMixin, ModelResponseMixin):
    default_values = {}

    def get_default_values(self):
        return dict(self.default_values)

    def new_object(self):
        return self.model(**self.get_default_values())

    @rest_api("", method="post")
    def post(self, *args, **kwargs):
        obj = self.new_object()
        data = self.get_model_data(obj, self.deserialize_body(), created=True)
        resolver = ObjectResolver(obj)
        resolver.set_values(**data)
        try:
            self.validate(resolver, created=True)
            return self.is_valid(resolver, created=True)
        except ValidationError as e:
            return self.is_invalid(resolver, errors=e)


class UpdateRestViewMixin(ModelBodyMixin, ModelResponseMixin):
    @rest_api("/<int:id>", method="put")
    def put(self, id, *args, **kwargs):
        obj = self.get_object(pk=id)
        data = self.get_model_data(obj, self.deserialize_body(), created=False)
        resolver = ObjectResolver(obj)
        resolver.set_values(**data)
        try:
            self.validate(resolver, created=False)
            return self.is_valid(resolver, created=False)
        except ValidationError as e:
            return self.is_invalid(resolver, errors=e)


class DeleteRestViewMixin(ModelMixin):
    @rest_api("/<int:id>", method="delete")
    def delete(self, id, *args, **kwargs):
        obj = self.get_object(pk=id)
        try:
            with transaction.atomic():
                obj.delete()
            return self.message_response(f(
                _("{model} {obj} deleted."), model=self.model_name, obj=obj))
        except IntegrityError as e:
            logger.debug("IntegrityError: %s", e)
            raise APIError(f(_(
                "{obj} cannot be deleted because "
                "it is referenced by other objects."), obj=obj))


class MediaRestViewMixin(ModelMixin):
    def _get_model_field(self, field):
        try:
            model_field = self.model._meta.get_field(field)
            if not isinstance(model_field, MediaField):
                raise NotFoundError  # pragma: no cover
        except FieldDoesNotExist:  # pragma: no cover
            raise NotFoundError
        return model_field

    @rest_api("/<int:pk>/<str:field>/upload-url/<str:filename>", method="get")
    def field_media_upload_url(self, pk, field, filename, *args, **kwargs):
        obj = self.get_object(pk=pk)
        try:
            res = self._get_model_field(field).get_upload_url(
                self.request, obj, filename)
        except StorageException as e:  # pragma: no cover
            logger.exception(e)
            raise APIError(_("Unexpected storage error", status=500))
        return JsonResponse(res)

    @rest_api("/<int:pk>/<str:field>", method="get")
    def field_media_get(self, pk, field, *args, **kwargs):
        obj = self.get_object(pk=pk)
        try:
            url = self._get_model_field(field).get_url(self.request, obj)
        except StorageException as e:  # pragma: no cover
            logger.exception(e)
            raise APIError(_("Unexpected storage error", status=500))
        if self.request.GET.get('redirect', '0').lower() in ['0', 'false']:
            return JsonResponse(dict(url=url))
        return redirect(url)


class SecuredRestViewMixin(View):
    default_public = False

    def perm(self):
        return True

    def _is_public(self, public, func_name):
        param = f'{func_name}_public'
        if hasattr(self, param):
            public = getattr(self, param)
        if public is None:
            public = self.default_public
        return public

    def check_perm(self, public, func_name, *args, **kwargs):
        if self._is_public(public, func_name):
            return
        if not self.request.user.is_authenticated:
            raise UnauthorizedError()
        if not self.perm():
            raise ForbiddenError()
        fperm = f'{func_name}_perm'
        if hasattr(self, fperm) and not getattr(self, fperm)(*args, **kwargs):
            raise ForbiddenError()


class BaseRestView(SecuredRestViewMixin, View):
    pass


class RestView(
        ListRestViewMixin,
        DetailRestViewMixin,
        CreateRestViewMixin,
        UpdateRestViewMixin,
        DeleteRestViewMixin,
        BaseRestView):
    pass
