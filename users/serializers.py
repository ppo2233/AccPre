from rest_framework import serializers
from users.models import UserProfile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """ 用户扩展序列化 """
    class Meta:
        model = UserProfile
        fields = '__all__'
