import traceback

from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from accpre.core.responses import Response
from accpre.core.exceptions import AccPreException
from accpre.core import status_codes
from accpre.core.utils import Utils


class AccPreGenericValidate:
    """ AccPre 通用验证 """

    def generic_err_msg(self, code, param_info):
        """ 通用的error msg 提示 """

        return Utils.json_dumps({
            'err_code': code,
            'msg': status_codes.CODE_MSG[code].format(param=param_info)
        })

    def validate_param_is_none(self, param_value, param_name):
        """ 验证参数是否为空 """
        if Utils.is_param_none(param_value):
            raise AccPreException(
                self.generic_err_msg(
                    status_codes.PARAM_IS_NULL_CODE, param_name
                )
            )

    def validate_param_length(self, param_value, param_name):
        """ 验证字符长度 """
        if not Utils.is_allow_length(param_value):
            raise AccPreException(
                self.generic_err_msg(
                    status_codes.PARAM_LENGTH_ERR_CODE, param_name
                )
            )

    def validate_name_is_duplicate(self, model, param_name, pk=None, **params):
        """ 验证名称是否重复 """
        if pk is None:
            if model.objects.filter(**params):
                raise AccPreException(
                    self.generic_err_msg(
                        status_codes.PARAM_IS_DUPLICATED, param_name
                    )
                )


class AccPreBaseViewSets(viewsets.ModelViewSet, AccPreGenericValidate):
    """  AccPre Base ViewSets """
    authentication_classes = [OAuth2Authentication]


class AccPreViewSets(AccPreBaseViewSets):
    """ AccPre ViewSets """
    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        pass

    def after_create(self, instance, request, *args, **kwargs):
        """ 创建后 """
        pass

    def perform_create(self, serializer):
        """ 执行创建保存 """
        return serializer.save()

    def create(self, request, *args, **kwargs):
        """ rewrite Create a model instance. """
        self.before_create(request, *args, **kwargs)  # 添加创建前钩子
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.after_create(instance, request, *args, **kwargs)  # 添加创建后钩子
        return Response(data=serializer.data, headers=headers)
