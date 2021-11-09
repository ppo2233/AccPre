import traceback
import logging

from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import model_to_dict

from accpre.core.responses import Response
from accpre.core.viewsets import AccPreViewSets
from users.models import UserProfile, Menu
from users.serializers import UserProfileSerializer
from accpre import settings
from accpre.core.utils import Utils
from accpre.core.exceptions import AccPreException
from accpre.core import status_codes


logger = logging.getLogger(__name__)


class UserProfileViewSet(AccPreViewSets):
    """ 用户 """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    fields = ['name', 'role', 'failed', 'created', 'modified']

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

    def after_create(self, instance, request, *args, **kwargs):  # 添加创建后钩子
        self.create_token_group(instance.user.username)  # 创建令牌组

    def before_update(self, userprofile_instance):
        """ 修改 """
        password = self.request.data.get('password', None)
        name = self.request.data.get('name', userprofile_instance.name)
        self.validate_name(name, pk=userprofile_instance.id)
        self.update_auth_user(userprofile_instance, password)

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

    def update_auth_user(self, userprofile_instance, password):
        """ 修改用户 """
        self.update_password(userprofile_instance, password)  # 修改密码

    def update_password(self, userprofile_instance, password):
        """ 修改密码 """
        if userprofile_instance and password:
            user = userprofile_instance.user
            user.set_password(password)
            user.save()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ rewrite Create a model instance. """
        try:
            _, data = self.before_create(request, *args, **kwargs)
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

    def validate_name(self, name, pk=None):
        """ 用户昵称验证 """
        self.validate_param_is_none(name, 'name')
        self.validate_param_length(name, 'name')
        self.validate_name_is_duplicate(UserProfile, 'name', pk=pk, **{'name': name})

    def validates(self, user_profile, username, name):
        """ 验证 """
        self.validate_role(user_profile)  # 用户角色验证
        self.validate_username(username)  # 用户登录名验证
        self.validate_name(name)  # 用户昵称验证

    def update(self, request, *args, **kwargs):
        """ 重写修改方法 """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            self.before_update(instance)  # 修改前钩子
            data = self.get_request_mutable_data(request)
            if 'user' not in data:
                data['user'] = instance.user.id
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            self.after_update(instance)  # 修改后钩子
        except AccPreException as ae:
            ae = Utils.json_loads(str(ae))
            return Response(msg=ae['msg'], err_code=ae['err_code'])
        except Exception as e:
            return Response(err_code=status_codes.UNKNOWN_ERROR, msg=str(e))
        return Response(serializer.data)

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

    def get_top_menus(self):
        """ 获取顶级菜单 """
        order = self.get_default_order_filed()
        return [m for m in Menu.objects.filter(parent=None).exclude(name='').order_by(order)]

    def get_sub_menus(self, parents):
        """ 获取子菜单 """
        order = self.get_default_order_filed()
        data = []
        for p in parents:  # 一级菜单
            p_dict = model_to_dict(p)
            p_dict['subs'] = []
            subs = Menu.objects.filter(parent=p).exclude(name='').order_by(order)
            for s in subs:  # 二级菜单
                s_dict = model_to_dict(s)
                p_dict['subs'].append(s_dict)
            data.append(p_dict)
        return data

    def get_default_order_filed(self):
        """ 获取默认排序字段 """
        return 'priority'

    @action(methods=['post'], detail=False)
    def get_menus(self, request):
        """ 获取菜单 """
        try:
            first_levels = self.get_top_menus()
            data = self.get_sub_menus(first_levels)
        except Exception as e:
            code = status_codes.UNKNOWN_ERROR
            return Response(err_code=code, msg=f'{e}')
        return Response(data)
