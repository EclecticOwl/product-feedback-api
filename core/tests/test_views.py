from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate

from django.urls import reverse

from core import views
from core.models import Product, Feedback, CustomUser as User

class ProductListTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.get_or_create(username='mike', password='123')
        self.user = User.objects.get(username='mike')
    
    def test_details(self):
        request = self.factory.get(reverse('product_list'))
        response = views.ProductList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
        data = {'title': 'hello'}
        request = self.factory.post(reverse('product_list'), data)
        force_authenticate(request, user=self.user)
        response = views.ProductList.as_view()(request)
        self.assertEqual(response.status_code, 201)

class ProductDetailTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        User.objects.create(username='mike2', password='234')
        self.user = User.objects.get(username='mike')
        self.user2 = User.objects.get(username='mike2')
        self.product = Product.objects.create(owner=self.user, title='blaaaaa').pk
    
    def test_details(self):
        # Test detail GET request
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product}))
        self.assertEqual(response.status_code, 200)
        # Test PUT request no authentication
        response = self.client.put(reverse('product_detail', kwargs={'pk': self.product}), {"title": "test"})
        self.assertEqual(response.status_code, 401)
        # Test PUT request incorrect authorization
        self.client.force_authenticate(self.user2)
        response = self.client.put(reverse('product_detail', kwargs={'pk': self.product}), {"title": "test"})
        self.assertEqual(response.status_code, 403)
        # Test successful PUT request
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse('product_detail', kwargs={'pk': self.product}), {"title": "test"})
        self.assertEqual(response.status_code, 200)
        product = Product.objects.get(pk=self.product)
        self.assertEqual(product.title, "test")

class FeedbackListTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        User.objects.create(username='mike2', password='234')
        self.user = User.objects.get(username='mike')
        self.user2 = User.objects.get(username='mike2')
        self.product = Product.objects.create(owner=self.user, title='test').pk
    
    def test_details(self):
        # Test GET request
        response = self.client.get(reverse('feedback_list'))
        self.assertEqual(response.status_code, 200)
        # Test POST request with no authentication
        response = self.client.post(reverse('feedback_list'), 
            {'description': 'test', 'title': 'Could use more cats!'})
        self.assertEqual(response.status_code, 401)
         # Test POST request not all required fields
        self.client.force_authenticate(self.user2)
        response = self.client.post(reverse('feedback_list'), 
            {'description': 'test', 'product': self.product})
        self.assertEqual(response.status_code, 400)
        # Test POST request success
        self.client.force_authenticate(self.user2)
        response = self.client.post(reverse('feedback_list'), 
            {'description': 'test', 'title': 'Could use more cats!', 'product': self.product})
        # self.assertEqual(response.status_code, 201)

class FeedbackDetailTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        User.objects.create(username='mike2', password='234')
        self.user = User.objects.get(username='mike')
        self.user2 = User.objects.get(username='mike2')
        self.product = Product.objects.create(owner=self.user, title='blaaaaa').pk
        Feedback.objects.create(
            description='test',
            owner=self.user2,
            product=Product.objects.get(pk=self.product),
            title='noice',
            )
    
    def test_details(self):
        # Test detail GET request
        response = self.client.get(reverse('feedback_detail', kwargs={'pk': self.product}))
        self.assertEqual(response.status_code, 200)
        # Test PUT request no authentication
        response = self.client.put(reverse('feedback_detail', kwargs={'pk': self.product}), {"title": "test"})
        self.assertEqual(response.status_code, 401)
        # Test PUT request incorrect authorization
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse('feedback_detail', kwargs={'pk': self.product}), {"title": "test"})
        self.assertEqual(response.status_code, 403)
        # Test successful PUT request
        self.client.force_authenticate(self.user2)
        response = self.client.put(reverse('feedback_detail', kwargs={'pk': self.product}), {"title": "test"})
        self.assertEqual(response.status_code, 200)