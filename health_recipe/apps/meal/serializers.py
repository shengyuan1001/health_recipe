from rest_framework import serializers
from apps.meal.models import MealModel


# 管理员模型序列化
class MealModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealModel
        fields = "__all__"
