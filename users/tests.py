from rest_framework import status
from django.urls import reverse

from accpre.core.test import AccPreTest
from accpre.core.utils import Utils
from users.models import UserProfile


class UserTest(AccPreTest):
    """ User 的单元测试 """
    fixtures = ['00.initializer_menus.json']

    def setUp(self):
        super(UserTest, self).setUp()

        self.users_data = [
            {
                'username': 'super_admin',
                'password': 'super_admin_123',
                'email': 'super_admin@gmail.com'
            },
            {
                'username': 'admin_user',
                'password': 'admin_user_123',
                'email': 'admin_user@gmail.com'
            },
            {
                'username': 'common_user_01',
                'password': 'common_user_01_123',
                'email': 'common_user_01@gmail.com'
            },
            {
                'username': 'common_user_02',
                'password': 'common_user_02_123',
                'email': 'common_user_02@gmail.com'
            }
        ]
        self.users = self.create_instances(self.users_data, 'User')

        self.user_profiles = self.create_instances([
            {
                'name': 'super_admin',
                'role': 1,
                'user': self.users[0]
            },
            {
                'name': 'admin_user',
                'role': 2,
                'user': self.users[1]
            },
            {
                'name': 'common_user_01',
                'role': 3,
                'user': self.users[2]
            },
            {
                'name': 'common_user_01',
                'role': 3,
                'user': self.users[3]
            }
        ], 'UserProfile')

    def test_login_user(self):
        """
        测试用户登录用例：
            # 账号密码正确
            # 账号有误
            # 密码有误
        """
        # 账号密码正确
        url = reverse('users:userprofile-login')
        data = {
            'username': self.users[0].username,
            'password': self.users_data[0]['password']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertTrue(response_data['data']['token'], response_data)

        # 账号有误
        url = reverse('users:userprofile-login')
        data = {
            'username': 'error',
            'password': self.users_data[0]['password']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0100', response_data)
        self.assertIn('username', response_data['msg'], response_data)

        # 密码有误
        url = reverse('users:userprofile-login')
        data = {
            'username': self.users[0].username,
            'password': 'error'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0100', response_data)
        self.assertIn('password', response_data['msg'], response_data)

    def test_create_user(self):
        """
        测试创建用户用例：
            # token权限认证
            # 昵称为空
            # 昵称重复
            # 昵称字符超过20
            # 登录名为空
            # 登录名重复
            # 登录名字符超过20
            # 正常创建（超级管理员）
            # TODO 密码为空
            # TODO 密码不一致
        """
        url = reverse('users:userprofile-list')

        # token权限认证
        data = {
            'name': 'xq_00',
            'username': 'xq_00',
            'password': 'xq_00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.content)

        # 昵称为空
        data = {
            'name': '',
            'username': 'xq_01',
            'password': 'xq_01'
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0001', response_data)
        self.assertIn('name', response_data['msg'], response_data)

        # 昵称重复
        data = {
            'name': self.user_profiles[0].name,
            'username': 'xq_01',
            'password': 'xq_01'
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0002', response_data)
        self.assertIn('name', response_data['msg'], response_data)

        # 昵称字符超过20
        data = {
            'name': '123456789012345678901',
            'username': 'xq_02',
            'password': 'xq_02'
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0003', response_data)
        self.assertIn('name', response_data['msg'], response_data)

        # 登录名为空
        data = {
            'name': 'xq_03',
            'username': '',
            'password': 'xq_03'
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0001', response_data)
        self.assertIn('username', response_data['msg'], response_data)

        # 登录名重复
        data = {
            'name': 'xq_04',
            'username': self.users[0].username,
            'password': 'xq_04'
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0002', response_data)
        self.assertIn('username', response_data['msg'], response_data)

        # 登录名字符超过20
        data = {
            'name': 'xq_05',
            'username': '123456789012345678901',
            'password': 'xq_05'
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0003', response_data)
        self.assertIn('username', response_data['msg'], response_data)

        # 正常创建（超级管理员）
        data = {
            'name': 'xq_06',
            'username': 'xq_06',
            'password': 'xq_06',
            'role': 1
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        validate_data = response_data['data']
        self.assertEqual(validate_data['name'], data['name'], validate_data)
        self.assertEqual(validate_data['role'], 1, validate_data)

    def test_update_user(self):
        """
        测试修改用户用例：
            # 昵称为空
            # 昵称字符超过20
            # 密码为空
            # 密码不一致
        """

        # 修改前登录验证
        url_1 = reverse('users:userprofile-login')
        password_1 = 'super_admin_123'
        data_1 = {
            'username': self.users[0].username,
            'password': password_1
        }

        response = self.client.post(url_1, data=data_1, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertTrue(response_data['data']['token'], response_data)

        # 修改密码
        data_2 = {
            'password': 'super_admin_123_update'
        }
        url = reverse('users:userprofile-detail', args=(self.user_profiles[0].id, ))
        response = self.client.put(url, data_2, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)

        # 修改密码后登录验证
        response = self.client.post(url_1, data=data_1, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0100', response_data)
        self.assertIn('password is error', response_data['msg'], response_data)

    def test_destroy_user(self):
        """ 测试删除用户 """
        self.assertEqual(UserProfile.objects.all().count(), 6)
        pk = self.user_profiles[0].id
        url = reverse('users:userprofile-detail', args=(pk,))
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.assertEqual(UserProfile.objects.all().count(), 5)
        self.assertFalse(UserProfile.objects.filter(pk=pk))

    def test_user_query(self):
        """ 测试用户查询 """
        # 查询列表
        url = reverse("users:userprofile-list")
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['count'], 6, response_data)

        # 模糊查询
        url = '{}{}'.format(reverse("users:userprofile-list"), '?name=name_')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['count'], 2, response_data)

        # 分页
        url = '{}{}'.format(reverse("users:userprofile-list"), '?offset=0&limit=1')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(len(response_data['results']), 1, response_data)
        self.assertEqual(response_data['count'], 6, response_data)
        self.assertTrue(response_data['next'], response_data)

        # 分页排序
        url = '{}{}'.format(reverse("users:userprofile-list"), '?offset=0&limit=2&order=-name')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['results'][0]['name'], 'super_admin')
        self.assertEqual(len(response_data['results']), 2, response_data)
        self.assertEqual(response_data['count'], 6, response_data)
        self.assertTrue(response_data['next'], response_data)

        url = '{}{}'.format(reverse("users:userprofile-list"), '?offset=0&limit=2&order=name')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['results'][0]['name'], 'admin_user')
        self.assertEqual(len(response_data['results']), 2, response_data)
        self.assertEqual(response_data['count'], 6, response_data)
        self.assertTrue(response_data['next'], response_data)

    def test_get_menus(self):
        """ 测试获取菜单 """
        url = reverse('users:userprofile-get-menus')
        response = self.client.post(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
