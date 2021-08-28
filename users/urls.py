from django.conf.urls import url, include
from rest_framework import routers

from users import views

app_name = 'users'
router = routers.DefaultRouter()

router.register(r'users', views.UserProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
