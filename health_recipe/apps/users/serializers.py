from django.contrib.auth.models import User
from rest_framework import serializers


# 管理员模型序列化
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
