import traceback

from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

from accpre.core.responses import Response
from accpre.core.exceptions import AccPreException
from accpre.core import status_codes
from accpre.core.utils import Utils
from accpre import settings


class AccPreGenericValidate:
    """ AccPre 通用验证 """

    def generic_err_msg(self, code, param_info):
        """ 通用的error msg 提示 """

        return Utils.json_dumps({
            'err_code': code,
            'msg': status_codes.CODE_MSG[code].format(param=param_info)
        })

    def _raise(self, code, mgs, raisor=AccPreException):
        """ 抛出异常 """
        raise raisor(self.generic_err_msg(code, mgs))

    def validate_param_is_none(self, param_value, param_name):
        """ 验证参数是否为空 """
        if Utils.is_param_none(param_value):
            self._raise(status_codes.PARAM_IS_NULL_CODE, param_name)

    def validate_param_length(self, param_value, param_name):
        """ 验证字符长度 """
        if not Utils.is_allow_length(param_value):
            self._raise(status_codes.PARAM_LENGTH_ERR_CODE, param_name)

    def validate_name_is_duplicate(self, model, param_name, pk=None, **params):
        """ 验证名称是否重复 """
        query = model.objects.filter(**params)
        if pk is not None:
            query = query.exclude(pk=pk)
        if query:
            self._raise(status_codes.PARAM_IS_DUPLICATED, param_name)


class AccPreBaseViewSets(viewsets.ModelViewSet, AccPreGenericValidate):
    """  AccPre Base ViewSets """
    authentication_classes = [OAuth2Authentication]


class AccPreViewSets(AccPreBaseViewSets):
    """ AccPre ViewSets """
    order = settings.DEFAULT_ORDER
    fields = []

    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        pass

    def after_create(self, instance, request, *args, **kwargs):
        """ 创建后 """
        pass

    def before_delete(self):
        """ 删除前 """
        pass

    def after_delete(self):
        """ 删除后 """
        pass

    def before_update(self, instance):
        """ 修改前 """
        pass

    def after_update(self, instance):
        """ 修改后 """
        pass

    def perform_create(self, serializer):
        """ 执行创建保存 """
        return serializer.save()

    def create(self, request, *args, **kwargs):
        """ 重写创建方法 """
        try:
            self.before_create(request, *args, **kwargs)  # 添加创建前钩子
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            self.after_create(instance, request, *args, **kwargs)  # 添加创建后钩子

        except AccPreException as ae:
            ae = Utils.json_loads(str(ae))
            return Response(msg=ae['msg'], err_code=ae['err_code'])

        except Exception as e:
            return Response(err_code=status_codes.UNKNOWN_ERROR, msg=str(e))

        return Response(data=serializer.data, headers=headers)

    def list(self, request, *args, **kwargs):
        """ 重写查询方法 """
        self.order = request.query_params.get('order', self.order)  # 排序字段
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)  # 分页

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def filter_queryset(self, queryset):
        """ 重写过滤器 """
        for field in self.fields:
            value = self.request.query_params.get(field, None)

            if field in settings.CONTAINS_QUERY_FIELDS and value:  # 模糊查询
                queryset = queryset.filter(**{f'{field}__contains': value})

        queryset = queryset.order_by(self.order)  # 排序
        return queryset

    def destroy(self, request, *args, **kwargs):
        """ 重写删除方法 """
        try:
            instance = self.get_object()
            self.before_delete()  # 删除前
            self.perform_destroy(instance)
            self.after_delete()  # 删除后

        except AccPreException as ae:
            ae = Utils.json_loads(str(ae))
            return Response(msg=ae['msg'], err_code=ae['err_code'])

        except Exception as e:
            return Response(err_code=status_codes.UNKNOWN_ERROR, msg=str(e))

        return Response()

    def update(self, request, *args, **kwargs):
        """ 重写修改方法 """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            self.before_update(instance)  # 修改前钩子
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            self.after_update(instance)  # 修改后钩子

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

        except AccPreException as ae:
            ae = Utils.json_loads(str(ae))
            return Response(msg=ae['msg'], err_code=ae['err_code'])

        except Exception as e:
            return Response(err_code=status_codes.UNKNOWN_ERROR, msg=str(e))

        return Response(serializer.data)
