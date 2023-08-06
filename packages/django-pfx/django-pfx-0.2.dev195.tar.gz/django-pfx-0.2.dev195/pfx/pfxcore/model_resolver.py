import logging
import operator

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.constants import LOOKUP_SEP
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class PropertyField:
    def __init__(self, field_name, prop):
        self.name = field_name
        if hasattr(prop, 'fget'):
            self.verbose_name = getattr(
                prop.fget, 'short_description', prop.fget.__name__)
            self.internal_type = getattr(prop.fget, 'internal_type', None)
        else:
            self.verbose_name = (
                hasattr(prop, 'name') and prop.name or str(prop))
            self.internal_type = None

    def get_internal_type(self):
        return self.internal_type


class VirtualField:
    def __init__(self, field_descr):
        if isinstance(field_descr, tuple):
            self.name, self.verbose_name, self.internal_type = field_descr
        else:
            self.name = field_descr
            self.verbose_name = field_descr
            self.internal_type = None

    def get_internal_type(self):
        return self.internal_type


class MetaResolver:
    def __init__(self, model):
        self.model = model

    def get_field(self, field_descr):
        if isinstance(field_descr, tuple):
            return VirtualField(field_descr)
        lookup = field_descr
        path = lookup.split(LOOKUP_SEP)
        path, field_name = path[:-1], path[-1]
        model = self.model
        for e in path:
            model = model._meta.get_field(e).related_model
        try:
            attr = getattr(model, field_name)
        except AttributeError:
            return VirtualField(field_name)
        if isinstance(attr, property):
            return PropertyField(field_name, attr)
        if isinstance(attr, cached_property):
            return PropertyField(field_name, attr)
        return model._meta.get_field(field_name)


class ObjectResolver:
    def __init__(self, object):
        self.object = object

    def get_value(self, field_descr):
        try:
            lookup = (
                isinstance(field_descr, tuple) and field_descr[0] or
                field_descr)
            return operator.attrgetter(
                lookup.replace(LOOKUP_SEP, '.'))(self.object)
        except ObjectDoesNotExist:
            return

    def set_value(self, field_name, value):
        try:
            setattr(self.object, field_name, value)
        except AttributeError:
            raise Exception(
                f"Cannot set property {field_name} of "
                f"{self.object.__module__}{self.object.__class__.__name__}")

    def set_values(self, **values):
        for fname, value in values.items():
            self.set_value(fname, value)

    def validate(self, **kwargs):
        self.object.full_clean(**kwargs)

    def save(self):
        self.object.save()
