from django.contrib import admin

# Register your models here.
from apps.recipe.models import *


class ContactClassFoodModel(admin.ModelAdmin):
    list_display = ['name', 'show_img']
    list_filter = ['name']


class ContactFoodModel(admin.ModelAdmin):
    list_display = ['name', 'class_name', 'calorie', 'vitamin_a', 'vitamin_c', 'vitamin_e', 'vitamin_b1', 'vitamin_b2',
                    'protein', 'axunge', 'carbohydrate', 'dietary_fiber', 'show_img']
    list_filter = ['name', 'calorie']


class ContactRecipeModel(admin.ModelAdmin):
    list_display = ['r_name', ]
    list_filter = ['r_name']


admin.site.register(ClassFoodModel, ContactClassFoodModel)
admin.site.register(FoodModel, ContactFoodModel)
admin.site.register(RecipeModel, ContactRecipeModel)
