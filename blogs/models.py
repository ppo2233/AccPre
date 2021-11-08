from django.db import models
from users.models import UserProfile


class Link(models.Model):
    """ 链接表 """
    name = models.CharField('名称', max_length=255)
    url = models.CharField('url', default='', max_length=255)
    desc = models.CharField('描述', default='', max_length=255)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}({self.id})'


class Label(models.Model):
    """ 标签表 """
    name = models.CharField('名称', max_length=255)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}({self.id})'


class Classification(models.Model):
    """ 分类表 """
    name = models.CharField('名称', max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField('层数', default=0)
    is_root = models.BooleanField('是否为根', default=False)
    priority = models.IntegerField('优先级', default=0)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}({self.id})'


class Article(models.Model):
    """ 文章表 """
    name = models.CharField('名称', max_length=255)
    label = models.ManyToManyField(Label,
                                   related_name='articles',
                                   related_query_name='article',
                                   null=True, blank=True)
    classification = models.ForeignKey(Classification,
                                       related_name='articles',
                                       related_query_name='article',
                                       on_delete=models.CASCADE, null=True, blank=True)
    heat = models.IntegerField('热度', default=0)
    abstract = models.TextField('摘要', default='')
    content = models.TextField('内容', default='')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}({self.id})'
