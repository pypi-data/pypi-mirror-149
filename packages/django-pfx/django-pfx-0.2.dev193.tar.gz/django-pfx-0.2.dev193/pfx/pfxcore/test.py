import json
import logging
import re
from functools import reduce
from http.cookies import SimpleCookie

from django.test.client import Client as DjangoClient

logger = logging.getLogger(__name__)


def print_response(r, title="http response"):
    print(f"\n\n*********************{title}*********************")
    if not r:
        print("Response is null")
    print("Status : ", r.status_code, r.reason_phrase)
    print("Headers : ")
    print("".join(f"  {k}: {v}\n" for k, v in r.headers.items()))
    print("Content : ")
    if hasattr(r, 'json_content'):
        print(json.dumps(r.json_content, indent=4, sort_keys=True))
    elif hasattr(r, 'content') and r.content:
        print(r.content)
    elif hasattr(r, 'streaming_content'):
        print("Streaming content")
    else:
        print("Response is empty")
    print("*******************************************************\n\n")


class APIClient(DjangoClient):

    token = None
    default_locale = None
    auth_cookie = None

    def __init__(self, enforce_csrf_checks=False, raise_request_exception=True,
                 default_locale=None, with_cookie=False, **defaults):
        super().__init__(enforce_csrf_checks, raise_request_exception,
                         **defaults)
        self.default_locale = default_locale
        self.with_cookie = with_cookie

    def login(self, username, password='test',
              path='/api/auth/login', locale=None):
        self.token = None
        response = self.post(
            f"{path}{self.with_cookie and '?mode=cookie' or ''}", {
                'username': username,
                'password': password}, locale=locale)
        if response.status_code == 200:
            if self.with_cookie:
                self.auth_cookie = [
                    v for k, v in response.client.cookies.items()
                    if k == 'token'][0]
                regex = r".*token=([\w\._-]*);.*"
                self.token = re.findall(regex, str(self.auth_cookie))[0]
            else:
                self.token = response.json_content['token']
            return True
        return False

    def logout(self):
        self.token = None

    def generic(self, method, path, data='',
                content_type='application/octet-stream', secure=False,
                **extra):
        if self.token:
            if self.with_cookie:
                self.cookies = SimpleCookie(
                    {'token': self.token})
            else:
                extra.update(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        return super().generic(
            method, path, data, content_type, secure, **extra)

    def update_locale(self, locale, extra):
        nextra = dict(extra)
        if locale:
            nextra.update(HTTP_X_CUSTOM_LANGUAGE=f"{locale}")
        elif self.default_locale:
            nextra.update(HTTP_X_CUSTOM_LANGUAGE=f"{self.default_locale}")
        return nextra

    @staticmethod
    def decode_response(response):
        if response.headers['Content-Type'] == 'application/json':
            response.json_content = response.json()
        response.print = lambda: print_response(response)
        return response

    def get(self, path, data=None, secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(super().get(path, data, secure, **extra))

    def post(self, path, data=None, content_type='application/json',
             secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(
            super().post(path, data, content_type, secure, **extra))

    def head(self, path, data=None, secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(
            super().head(path, data, secure, **extra))

    def trace(self, path, secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(super().trace(path, secure, **extra))

    def options(self, path, data='', content_type='application/json',
                secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(
            super().options(path, data, content_type, secure, **extra))

    def put(self, path, data='', content_type='application/json',
            secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(
            super().put(path, data, content_type, secure, **extra))

    def patch(self, path, data='', content_type='application/json',
              secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(
            super().patch(path, data, content_type, secure, **extra))

    def delete(self, path, data='', content_type='application/json',
               secure=False, locale=None, **extra):
        extra = self.update_locale(locale, extra)
        return self.decode_response(
            super().delete(path, data, content_type, secure, **extra))


class TestAssertMixin:

    # assert response status code
    def assertRC(self, response, code):
        return self.assertEqual(response.status_code, code)

    def get_val(self, response, key):
        def _p(k):
            return int(k[1:]) if k[0] == '@' else k
        try:
            return reduce(lambda c, k: c[_p(k)], key.split("."),
                          response.json_content)
        except IndexError:
            print_response(response, f'Index Error for key "{key}"')
            raise Exception(f'Index Error for key "{key}"')
        except KeyError:
            print_response(response, f'Key Error for key "{key}"')
            raise Exception(f'Key Error for key "{key}"')

    # assert JSON content at key equals value
    def assertJE(self, response, key, value):
        return self.assertEqual(self.get_val(response, key), value)

    # assert JSON content at key not equals value
    def assertNJE(self, response, key, value):
        return self.assertNotEqual(self.get_val(response, key), value)

    # assert JSON array size
    def assertSize(self, response, key, size):
        return self.assertEqual(len(self.get_val(response, key)), size)


class MockBoto3Client:
    def generate_presigned_url(self, *args, **kwargs):
        params = kwargs.get('Params', {})
        return f"http://{params.get('Bucket')}/{params.get('Key')}"

    def head_object(self, *args, **kwargs):
        return dict(ContentLength=1000, ContentType="image/png")

    def delete_object(self, *args, **kwargs):
        pass
