import json
import uuid
import base64

from django.apps import apps
from oauth2_provider.models import get_application_model
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauthlib.oauth2.rfc6749.endpoints.pre_configured import Server

from accpre import settings


class Utils:
    """ AccPre工具 """

    @staticmethod
    def reverse_model(model):
        """ 反向模型 """
        arr_model = str(model._meta).split('.')
        return arr_model[-1], arr_model[0]

    @staticmethod
    def get_model_app_relations():
        """ 获取模型app """
        return dict(map(Utils.reverse_model, apps.get_models()))

    @staticmethod
    def get_model(app_label, model_name):
        """ 获取模型 """
        return apps.get_model(app_label, model_name)

    @staticmethod
    def json_loads(data):
        try:
            data = json.loads(data)
        except:
            pass
        return data

    @staticmethod
    def json_dumps(data, ensure_ascii=False):
        return json.dumps(data, ensure_ascii=ensure_ascii)

    @staticmethod
    def is_param_none(param):
        """ 判断参数是否为空 """
        return not str(param).strip() or param is None or param == 0

    @staticmethod
    def is_allow_length(param, length=settings.DEFAULT_VARCHAR_LENGTH):
        """ 判断字符长度是否符合 """
        return len(str(param).strip()) <= length

    @staticmethod
    def init_password_grant_application(name="Test Application",
                                        client_id=settings.CLIENT_ID,
                                        client_secret=settings.CLIENT_SECRET):
        Application = get_application_model()
        apps = Application.objects.filter(name=name)
        if not apps:
            app = Application(
                name=name,
                client_id=client_id,
                client_secret=client_secret,
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_PASSWORD,
            )
            app.save()
        else:
            app = apps[0]

        return app

    @staticmethod
    def get_random_client_secret():
        """ 获取随机客户端密码 """
        return {
            'client_id': str(uuid.uuid1()),
            'client_secret': str(uuid.uuid1())
        }

    @staticmethod
    def create_token(username, password, client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET):
        uri = settings.DEFAULT_OAUTH_TOKEN_URL
        http_method = settings.DEFAULT_OAUTH_TOKEN_REQUEST_METHOD
        body = settings.DEFAULT_OAUTH_TOKEN_BODY.format(username=username,
                                                        password=password,
                                                        client_id=client_id,
                                                        client_secret=client_secret)
        headers = {}
        extra_credentials = None
        headers, token, status_code = Server(OAuth2Validator()).create_token_response(uri,
                                                                                      http_method,
                                                                                      body,
                                                                                      headers,
                                                                                      extra_credentials)
        return {
            'headers': headers,
            'token': token,
            'status_code': status_code
        }
