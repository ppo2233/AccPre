from django.conf.urls import url, include
from rest_framework import routers

from blogs import views


app_name = 'blogs'
router = routers.DefaultRouter()

router.register(r'blogs', views.LabelViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

