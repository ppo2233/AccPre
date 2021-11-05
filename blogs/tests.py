from rest_framework import status
from django.urls import reverse

from accpre.core.test import AccPreTest
from accpre.core.utils import Utils
from blogs.models import Label


class LabelTest(AccPreTest):
    """ Blog测试 """
    def setUp(self):
        super(LabelTest, self).setUp()
        self.labels = self.create_instances([
            {'name': '标签01'},
            {'name': '标签02'}
        ], 'Label')

    def test_label_create(self):
        """ 测试标签创建 """
        # 正常创建
        data = {
            'name': '标签001'
        }
        url = reverse('blogs:label-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertEqual(response_data['data']['name'], data['name'], response_data)

        # 异常创建
        data = {
            'name': ''
        }
        url = reverse('blogs:label-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0001', response_data)
        self.assertIn('is null', response_data['msg'], response_data)

        # 重名创建
        data = {
            'name': '标签001'
        }
        url = reverse('blogs:label-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0002', response_data)
        self.assertIn('is duplicate', response_data['msg'], response_data)

    def test_label_delete(self):
        """ 测试删除 """
        url = reverse('blogs:label-detail', args=(self.labels[0].id,))
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        labels = Label.objects.all()
        self.assertFalse(labels.filter(pk=self.labels[0].id), labels)
        self.assertEqual(labels.count(), len(self.labels)-1, labels)

    def test_label_query(self):
        """ 查询 """
        url = reverse('blogs:label-list')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['count'], 2, response_data)
