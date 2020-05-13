from django.contrib import admin

# Register your models here.
from apps.recipe.models import *


class ContactClassFoodModel(admin.ModelAdmin):
    list_display = ['name', 'show_img']
    list_filter = ['name']


class ContactFoodModel(admin.ModelAdmin):
    list_display = ['name', 'class_name', 'f_calorie', 'show_img']
    list_filter = ['name', 'f_calorie']


class ContactRecipeModel(admin.ModelAdmin):
    list_display = ['r_name', 'r_food1', 'r_food2', 'r_food3', 'r_food4', 'r_food5']
    list_filter = ['r_name']


admin.site.register(ClassFoodModel, ContactClassFoodModel)
admin.site.register(FoodModel, ContactFoodModel)
admin.site.register(RecipeModel, ContactRecipeModel)
