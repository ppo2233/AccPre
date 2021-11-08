from rest_framework import serializers
from blogs.models import Label, Classification, Link, Article


class LabelSerializer(serializers.ModelSerializer):
    """ 标签序列化 """
    class Meta:
        model = Label
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    """ 链接序列化 """
    class Meta:
        model = Link
        fields = '__all__'


class ClassificationSerializer(serializers.ModelSerializer):
    """" 分类序列化 """
    class Meta:
        model = Classification
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """" 文章序列化 """
    class Meta:
        model = Article
        fields = '__all__'
