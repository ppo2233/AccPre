import traceback

from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction

from accpre.core.responses import Response
from accpre.core.viewsets import AccPreViewSets
from users.models import UserProfile
from users.serializers import UserProfileSerializer
from accpre import settings
from accpre.core.utils import Utils
from accpre.core.exceptions import AccPreException
from accpre.core import status_codes


class UserProfileViewSet(AccPreViewSets):
    """ 用户 """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        user_profile = request.user.user_profiles
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)

        self.validates(user_profile, username, name)
        user = self.create_auth_user(username, password)  # 创建auth user
        data = self.get_request_mutable_data(request)
        data['user'] = user.id

        return user, data

    def get_request_mutable_data(self, request):
        """ 获取可边data """
        data = request.data
        try:
            data._mutable = True
        except:
            pass
        return data

    def create_auth_user(self, username, password):
        """ 创建auth user """
        return User.objects.create_user(username=username, password=password)

    def after_create(self, instance, request, *args, **kwargs):  # 添加创建后钩子
        self.create_token_group(instance.user.username)  # 创建令牌组

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ rewrite Create a model instance. """
        try:
            _, data = self.before_create(request, *args, **kwargs)  # 添加创建前钩子
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            self.after_create(instance, request, *args, **kwargs)
        except AccPreException as ae:
            ae = Utils.json_loads(str(ae))
            return Response(msg=ae['msg'], err_code=ae['err_code'])

        except Exception as e:
            return Response(msg=str(e), err_code=status_codes.UNKNOWN_ERROR)

        return Response(data=serializer.data, headers=headers)

    def create_token_group(self, username):
        """ 创建令牌组 """
        cs = Utils.get_random_client_secret()
        Utils.init_password_grant_application(username, cs['client_id'], cs['client_secret'])

    def validate_role(self, user_profile):
        """ 角色验证 """
        if user_profile.role in [settings.USER_ROLE_COMMON]:  # 普通用户
            err_code = status_codes.USER_ROLE_ERROR_CODE
            err_info = {err_code: status_codes.CODE_MSG[err_code]}
            raise AccPreException(Utils.json_dumps(err_info))

    def validate_username(self, username):
        """ 用户登录名验证 """
        self.validate_param_is_none(username, 'username')
        self.validate_param_length(username, 'username')
        self.validate_name_is_duplicate(User, 'username', **{'username': username})

    def validate_name(self, name):
        """ 用户昵称验证 """
        self.validate_param_is_none(name, 'name')
        self.validate_param_length(name, 'name')
        self.validate_name_is_duplicate(UserProfile, 'name', **{'name': name})

    def validates(self, user_profile, username, name):
        """ 验证 """
        self.validate_role(user_profile)  # 用户角色验证
        self.validate_username(username)  # 用户登录名验证
        self.validate_name(name)  # 用户昵称验证

    @action(methods=['post'], detail=False)
    def login(self, request):
        """ 登录 """
        try:
            username = request.data.get('username', None)
            password = request.data.get('password', None)

            user = authenticate(request, username=username, password=password)
            if not user:
                code = status_codes.USER_OR_PASSWORD_ERROR_CODE
                return Response(err_code=code, msg=status_codes.CODE_MSG[code])

            res = Utils.create_token(username, password)

        except Exception as e:
            code = status_codes.UNKNOWN_ERROR
            return Response(err_code=code, msg=f'{e}')

        return Response(res)
