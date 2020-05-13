#  -*- codeing: utf-8 -*- #
# 作者: bob
# 日期: 2020/5/9
from rest_framework.routers import SimpleRouter

from apps.recipe.views import *

Recipe_router = SimpleRouter()
Recipe_router.register(r'classfood', ClassFoodViewSet)
Recipe_router.register(r'food', FoodViewSet)
Recipe_router.register(r'recipe', RecipeViewSet)
