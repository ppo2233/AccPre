from rest_framework import status
from django.urls import reverse

from accpre.core.test import AccPreTest
from accpre.core.utils import Utils


class UserTest(AccPreTest):
    """ User 的单元测试 """
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
            # 正常创建（超级管理员）（用户权限）
            # TODO 密码为空
            # TODO 密码不一致
            # TODO 正常创建（管理员）（用户权限）
            # TODO 非管理用户创建（用户权限）
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

        # 正常创建（超级管理员）（用户权限）
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

    def test_update_user(self):
        """
        测试修改用户用例：
            # 昵称为空
            # 昵称字符超过20
            # 登录名为空
            # 登录名字符超过20
            # 密码为空
            # 密码不一致
            # 正常修改（当前用户）（用户权限）
            # 正常修改（超级管理员）（用户权限）
            # 异常修改（管理员操作其他用户）（用户权限）
            # 非管理员非当前用户修改（用户权限）
        """

    def test_destroy_user(self):
        """
        测试删除用户用例：
            # 正常删除（当前用户）（用户权限）
            # 正常删除（超级管理员）（用户权限）
            # 异常删除（管理员操作其他用户）（用户权限）
            # 非管理员非当前用户修改（用户权限）
        """

    def test_user_query(self):
        """ 测试用户查询 """
