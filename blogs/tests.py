from rest_framework import status
from django.urls import reverse

from accpre.core.test import AccPreTest
from accpre.core.utils import Utils
from blogs.models import Label, Link, Article


class BlogsTest(AccPreTest):
    """ Blogs测试 """
    def setUp(self):
        super(BlogsTest, self).setUp()
        self.labels = self.create_instances([
            {'name': '标签01'},
            {'name': '标签02'}
        ], 'Label')
        self.links = self.create_instances([
            {'name': '链接01', 'url': 'www.bookqiang.cn'},
            {'name': '链接02', 'url': 'www.baidu.com'}
        ], 'Link')
        self.first_classifications = self.create_instances([
            {'name': '一级分类01', 'level': 0, 'is_root': True, 'priority': 0},
            {'name': '一级分类02', 'level': 0, 'is_root': True, 'priority': 1},
        ], 'Classification')

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
        """ 测试标签删除 """
        url = reverse('blogs:label-detail', args=(self.labels[0].id,))
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        labels = Label.objects.all()
        self.assertFalse(labels.filter(pk=self.labels[0].id), labels)
        self.assertEqual(labels.count(), len(self.labels)-1, labels)

    def test_label_query(self):
        """ 测试标签查询 """
        url = reverse('blogs:label-list')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['count'], 2, response_data)

    def test_link_create(self):
        """ 测试链接创建 """
        # 正常创建
        data = {
            'name': '链接001',
            'url': 'www.baidu.com'
        }
        url = reverse('blogs:link-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertEqual(response_data['data']['name'], data['name'], response_data)

        # 异常创建
        data = {
            'name': '链接002',
            'url': ''
        }
        url = reverse('blogs:link-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0001', response_data)
        self.assertIn('url', response_data['msg'], response_data)
        self.assertIn('is null', response_data['msg'], response_data)

        # 重名创建
        data = {
            'name': '链接001',
            'url': 'www.baidu.com'
        }
        url = reverse('blogs:link-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], -1, response_data)
        self.assertEqual(response_data['err_code'], '0002', response_data)
        self.assertIn('name', response_data['msg'], response_data)
        self.assertIn('is duplicate', response_data['msg'], response_data)

    def test_link_delete(self):
        """ 测试链接删除 """
        url = reverse('blogs:link-detail', args=(self.links[0].id,))
        response = self.client.delete(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        links = Link.objects.all()
        self.assertFalse(links.filter(pk=self.labels[0].id), links)
        self.assertEqual(links.count(), len(self.labels)-1, links)

    def test_link_query(self):
        """ 测试链接查询 """
        url = reverse('blogs:link-list')
        response = self.client.get(url, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['count'], 2, response_data)

    def test_classification_create(self):
        """ 测试分类创建 """
        data = {
            'name': '一级分类001',
            'is_root': True
        }
        url = reverse('blogs:classification-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertEqual(response_data['data']['name'], data['name'])
        parent = response_data['data']['id']
        data = {
            'name': '二级分类001001',
            'parent': parent,
            'level': 1
        }
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertEqual(response_data['data']['name'], data['name'], response_data)
        self.assertEqual(response_data['data']['parent'], parent, response_data)
        self.assertEqual(response_data['data']['level'], data['level'], response_data)

    def test_article_create(self):
        """ 测试文章创建 """
        data = {
            'name': '文章001',
            'label': [self.labels[0].id, self.labels[1].id],
            'classification': self.first_classifications[0].id
        }
        url = reverse('blogs:article-list')
        response = self.client.post(url, data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = Utils.json_loads(response.content)
        self.assertEqual(response_data['code'], 0, response_data)
        self.assertEqual(data['name'], response_data['data']['name'], response_data)
        article = Article.objects.get(pk=response_data['data']['id'])
        labels = article.label.all()
        self.assertEqual(labels.count(), 2, labels)
        classification_id = article.classification.id
        self.assertEqual(classification_id, data['classification'], classification_id)
