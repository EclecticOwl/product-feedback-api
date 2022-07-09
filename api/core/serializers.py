from rest_framework import serializers
from .models import Product, Feedback, CustomUser



class FeedbackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Feedback
        fields = ['id', 'product', 'owner', 'title', 'category', 'upvotes', 'status', 'description']
        read_only_fields = ['id', 'owner', 'upvotes']
        depth = 1

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    feedback = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'owner', 'title', 'feedback']
        read_only_fields = ['id', 'owner']

class FeedbackUpvotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ['id', 'product', 'upvotes', 'owner']
        read_only_fields = ['id', 'owner']