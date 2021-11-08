from django.conf.urls import url, include
from rest_framework import routers

from blogs import views


app_name = 'blogs'
router = routers.DefaultRouter()

router.register(r'labels', views.LabelViewSet)
router.register(r'links', views.LinkViewSet)
router.register(r'classifications', views.ClassificationViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
