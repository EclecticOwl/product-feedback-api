from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from core.models import Product, Feedback
from core.serializers import ProductSerializer, FeedbackSerializer, FeedbackUpvotesSerializer
from core.permissions import IsOwnerOrReadOnly

from random import randint

@api_view(['GET'])
def api_root(request, format=None):
    """
    An API root directory for a brief overview of the endpoints.
    """
    return Response({
        'products': reverse('product_list', request=request, format=format),
        'feedback': reverse('feedback_list', request=request, format=format)
    })

class ProductList(APIView):
    """
    Lists all of the Product instances with GET, or can POST a single instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRandomView(APIView):
    def get(self, request, format=None):
        count = Product.objects.count()
        random_object = Product.objects.all()[randint(0, count - 1)]
        serializer = ProductSerializer(random_object)
        return Response(serializer.data)


class ProductDetail(APIView):
    """
    GET, PUT, and DELETE instances of Product.
    """

    permission_classes = [
        IsOwnerOrReadOnly,
        ]

    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(self.request, product)
            return product
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeedbackList(APIView):
    """
    Lists all of the Feedback instances with GET, or can POST a single instance.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        products = Feedback.objects.all()
        serializer = FeedbackSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(id=request.data['product'])
            serializer.save(owner=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackDetail(APIView):
    """
    GET, PUT, and DELETE instances of Feedback.
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        ]

    def get_object(self, pk):
        try:
            feedback = Feedback.objects.get(pk=pk)
            self.check_object_permissions(self.request, feedback)
            return feedback
        except Feedback.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        feedback = self.get_object(pk)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        feedback = self.get_object(pk)
        serializer = FeedbackSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        feedback = self.get_object(pk)
        feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeedbackUpvotes(APIView):
    """
    GET, PUT, and DELETE instances of Feedback.
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ]

    def get_object(self, pk):
        try:
            feedback = Feedback.objects.get(pk=pk)
            self.check_object_permissions(self.request, feedback)
            return feedback
        except Feedback.DoesNotExist:
            raise Http404
        
    def put(self, request, pk, format=None):
        feedback = self.get_object(pk)
        serializer = FeedbackUpvotesSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)