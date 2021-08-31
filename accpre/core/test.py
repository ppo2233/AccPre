import random

from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from accpre.core.utils import Utils


class AccPreTestCaseBase(APITestCase):
    """ AccPre Test Case Base """
    TEST_ADMIN_PASSWORD = 'admin123'

    def create_instances(self, instances, class_name):
        """ 创建 model instance """
        class_name = class_name.lower()
        results, relations = [], Utils.get_model_app_relations()

        for ins in instances:
            if class_name == 'user':
                model = User.objects.create_user(**ins)
            else:
                model_class = Utils.get_model(relations[class_name], class_name)
                model = model_class.objects.create(**ins)
            model.save()
            results.append(model)

        return results

    def setUp(self):
        """ 初始化 """
        # 初始化auth user
        self.users_data = [
            {
                'username': f'admin_01_{random.random()}',
                'password': self.TEST_ADMIN_PASSWORD
            },
            {
                'username': f'admin_02_{random.random()}',
                'password': self.TEST_ADMIN_PASSWORD
            }
        ]
        self.users = self.create_instances(self.users_data, 'User')

        # 初始化user_profile
        self.user_profiles = self.create_instances(
            [
                {
                    'name': f'name_01_{random.random()}',
                    'role': 1,
                    'user': self.users[0]
                },
                {
                    'name': f'name_02_{random.random()}',
                    'role': 2,
                    'user': self.users[1]
                }
            ], 'UserProfile'
        )


class AccPreTest(AccPreTestCaseBase):
    """ AccPre Test """
    def setUp(self):
        super().setUp()
        Utils.init_password_grant_application()  # 初始化测试令牌组
        res = Utils.create_token(self.users[0].username, self.users_data[0]['password'])  # 初始化token

        # 获取token请求头
        self.auth_header = {
            f"Authorization": "Bearer {}".format(
                Utils.json_loads(res['token'])['access_token']
            )
        }
