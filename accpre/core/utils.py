
from django.apps import apps


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
