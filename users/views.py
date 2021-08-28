from accpre.core.viewsets import AccPreViewSets
from users.models import UserProfile
from users.serializers import UserProfileSerializer


class UserProfileViewSet(AccPreViewSets):
    """ 用户 """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
