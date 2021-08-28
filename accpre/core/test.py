import random

from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from accpre.core.utils import Utils


class AccPreTestCaseBase(APITestCase):
    """ AccPre Test Case Base """

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
        self.users = self.create_instances([
            {
                'username': f'admin_01_{random.random()}',
                'password': 'admin123'
            },
            {
                'username': f'admin_02_{random.random()}',
                'password': 'admin123'
            }
        ], 'user')

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
    pass
