from rest_framework import serializers
from blogs.models import Label


class LabelSerializer(serializers.ModelSerializer):
    """ 标签序列化 """
    class Meta:
        model = Label
        fields = '__all__'
