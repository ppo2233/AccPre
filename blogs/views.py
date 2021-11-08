from blogs.models import Link, Label, Classification, Article
from accpre.core.viewsets import AccPreViewSets
from blogs.serializers import (
    LabelSerializer,
    LinkSerializer,
    ClassificationSerializer,
    ArticleSerializer
)


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


class LinkViewSet(AccPreViewSets):
    """ 链接 """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    fields = ['name', 'created', 'modified', 'url', 'desc']

    def validate_name(self, name):
        """ 验证名称 """
        self.validate_param_is_none(name, 'name')
        self.validate_param_length(name, 'name')
        self.validate_name_is_duplicate(Link, 'name', **{'name': name})

    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        name = request.data.get('name', None)
        url = request.data.get('url', None)
        self.validate_name(name)  # 名称验证
        self.validate_param_is_none(url, 'url')  # url验证


class ClassificationViewSet(AccPreViewSets):
    """ 分类 """
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    fields = ['name', 'created', 'modified', 'parent', 'level', 'is_root']

    def validate_name(self, name):
        """ 验证名称 """
        self.validate_param_is_none(name, 'name')
        self.validate_param_length(name, 'name')
        self.validate_name_is_duplicate(Classification, 'name', **{'name': name})

    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        name = request.data.get('name', None)
        self.validate_name(name)  # 名称验证


class ArticleViewSet(AccPreViewSets):
    """ 文章 """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    fields = ['name', 'label', 'classification', 'heat', 'status', 'created', 'modified']

    def validate_name(self, name):
        """ 验证名称 """
        self.validate_param_is_none(name, 'name')
        self.validate_param_length(name, 'name')
        self.validate_name_is_duplicate(Article, 'name', **{'name': name})

    def before_create(self, request, *args, **kwargs):
        """ 创建前 """
        name = request.data.get('name', None)
        self.validate_name(name)  # 名称验证
