from apps.recipe.models import *
from rest_framework import serializers


# 食物分类模型序列化
class ClassFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassFoodModel
        fields = "__all__"


# 食物模型序列化
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodModel
        fields = "__all__"


# 食谱模型序列化
class RecipeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeModel
        fields = "__all__"
