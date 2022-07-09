from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate

from core.models import CustomUser as User, Product, Feedback


class TestUserModel(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('test', 'test@test.com', '123')
        self.data = {'username': 'test@test.com', 'password': 'TestPassword####'}
    
    def test_can_create_user(self):
        self.client.login(username='test', password='123')
        response = self.client.post('/auth/users/', self.data)
        self.assertEqual(response.status_code, 201)

class TestProductModel(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='123')
        self.product = Product.objects.create(owner=self.user, title='Hello').pk
    
    def test_details(self):
        product = Product.objects.get(id=self.product)
        max_length = product._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

class TestFeedbackModel(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', password='123')
        self.product = Product.objects.create(owner=self.user, title='Hello')
        self.owner = User.objects.create(username='test2', password='234')

        self.feedback = Feedback.objects.create(
            product=self.product,
            owner=self.owner,
            title='Moooo',
            category='bug',
            status='suggestion',
            description='Moooooo'
        ).pk
    
    def test_details(self):
        feedback = Feedback.objects.get(id=self.feedback)
        self.assertEqual(str(feedback), 'Moooooo')
        self.assertEqual(feedback.product, self.product)
        self.assertEqual(feedback.owner, self.owner)

        max_length = feedback._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)
        self.assertEqual(feedback.title, 'Moooo')

        max_length = feedback._meta.get_field('category').max_length
        self.assertEqual(max_length, 20)
        self.assertEqual(feedback.category, 'bug')

        max_length = feedback._meta.get_field('status').max_length
        self.assertEqual(max_length, 12)
        self.assertEqual(feedback.status, 'suggestion')

        max_length = feedback._meta.get_field('description').max_length
        self.assertEqual(max_length, 400)
        self.assertEqual(feedback.description, 'Moooooo')

