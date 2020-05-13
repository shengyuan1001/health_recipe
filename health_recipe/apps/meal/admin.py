from django.contrib import admin

# Register your models here.
from apps.meal.models import MealModel


class ContactMealModel(admin.ModelAdmin):
    list_display = ['name', 'user', 'recipe', 'add_time']
    list_filter = ['name']


admin.site.register(MealModel, ContactMealModel)
