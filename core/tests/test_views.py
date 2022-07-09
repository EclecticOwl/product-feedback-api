from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate

from django.contrib.auth import get_user_model
from django.urls import reverse

from core import views
from core.models import Product, Feedback


User = get_user_model()

class ProductListTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        self.user = User.objects.get(id=1)
    
    def test_details(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('product_list'), 
            {'title': 'Could use more cats!'})

class ProductDetailTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        User.objects.create(username='mike2', password='234')
        self.user = User.objects.get(username='mike')
        self.user2 = User.objects.get(username='mike2')
        Product.objects.create(owner=self.user, title='blaaaaa')
    
    def test_details(self):
        # Test detail GET request
        response = self.client.get(reverse('product_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        # Test PUT request no authentication
        response = self.client.put(reverse('product_detail', kwargs={'pk': 1}), {"title": "test"})
        self.assertEqual(response.status_code, 401)
        # Test PUT request incorrect authorization
        self.client.force_authenticate(self.user2)
        response = self.client.put(reverse('product_detail', kwargs={'pk': 1}), {"title": "test"})
        self.assertEqual(response.status_code, 403)
        # Test successful PUT request
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse('product_detail', kwargs={'pk': 1}), {"title": "test"})
        self.assertEqual(response.status_code, 200)
        product = Product.objects.get(pk=1)
        self.assertEqual(product.title, "test")

class FeedbackListTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        User.objects.create(username='mike2', password='234')
        self.user = User.objects.get(username='mike')
        self.user2 = User.objects.get(username='mike2')
        Product.objects.create(owner=self.user, title='test')
    
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
            {'description': 'test', 'product': 1})
        self.assertEqual(response.status_code, 400)
        # Test POST request success
        self.client.force_authenticate(self.user2)
        response = self.client.post(reverse('feedback_list'), 
            {'description': 'test', 'title': 'Could use more cats!', 'product': 1})
        self.assertEqual(response.status_code, 201)

class FeedbackDetailTest(APITestCase):
    def setUp(self):
        User.objects.create(username='mike', password='234')
        User.objects.create(username='mike2', password='234')
        self.user = User.objects.get(username='mike')
        self.user2 = User.objects.get(username='mike2')
        Product.objects.create(owner=self.user, title='blaaaaa')
        Feedback.objects.create(
            description='test',
            owner=self.user2,
            product=Product.objects.get(id=1),
            title='noice',
            )
    
    def test_details(self):
        # Test detail GET request
        response = self.client.get(reverse('feedback_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        # Test PUT request no authentication
        response = self.client.put(reverse('feedback_detail', kwargs={'pk': 1}), {"title": "test"})
        self.assertEqual(response.status_code, 401)
        # Test PUT request incorrect authorization
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse('feedback_detail', kwargs={'pk': 1}), {"title": "test"})
        self.assertEqual(response.status_code, 403)
        # Test successful PUT request
        self.client.force_authenticate(self.user2)
        response = self.client.put(reverse('feedback_detail', kwargs={'pk': 1}), {"title": "test"})
        self.assertEqual(response.status_code, 200)