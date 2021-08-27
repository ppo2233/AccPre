from django.db import models
from django.contrib.auth.models import User

from accpre import settings


class UserProfile(models.Model):
    """ 用户扩展表 """
    name = models.CharField('昵称', max_length=255, default='')
    role = models.IntegerField('角色',
                               choices=settings.USER_ROLE_CHOICES,
                               default=settings.USER_ROLE_MANAGEMENT)
    failed = models.IntegerField('登录失败次数', default=0)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    owner = models.IntegerField('创建人', default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}({self.id})'


class Menu(models.Model):
    """ 菜单表 """
    name = models.CharField('菜单名', max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField('url', default='', max_length=255)
    level = models.IntegerField('层数', default=0)
    is_root = models.BooleanField('是否为根', default=False)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    modified = models.DateTimeField('修改时间', auto_now=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name}({self.id})'
