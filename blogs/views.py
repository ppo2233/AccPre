from blogs.models import Link, Label, Classification, Article
from accpre.core.viewsets import AccPreViewSets
from blogs.serializers import LabelSerializer


class LabelViewSet(AccPreViewSets):
    """ 标签 """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    fields = ['name', 'created', 'modified']

    def validate_name(self, name):
        """ 验证名称 """
        self.validate_param_is_none(name, 'name')
        self.validate_param_length(name, 'name')
        self.validate_name_is_duplicate(Label, 'name', **{'name': name})

    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        name = request.data.get('name', None)
        self.validate_name(name)
