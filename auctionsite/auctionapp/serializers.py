from rest_framework import serializers
from .models import Lot, AdminProfile, AuctionHistory, UserProfile


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AuctionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionHistory
        fields = '__all__'