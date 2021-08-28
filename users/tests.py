import json

from rest_framework import status
from django.urls import reverse

from accpre.core.test import AccPreTest


class UserTest(AccPreTest):
    """ User 的单元测试 """

    def test_user_query(self):
        """ 测试用户查询 """
        url = reverse('users:userprofile-list')
        response = self.client.get(url)

        response_data = json.loads(response.content)
        print('response -->', response_data)
