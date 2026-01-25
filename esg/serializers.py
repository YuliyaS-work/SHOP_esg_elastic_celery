from rest_framework import serializers

from .models import Order, Feedback, Electro, Gas, Santeh


class OrderSerializer(serializers.ModelSerializer):
    agreement = serializers.BooleanField(required=True)

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "mail",  "agreement")


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ("name", "phone", "subject", "message", "agreement")