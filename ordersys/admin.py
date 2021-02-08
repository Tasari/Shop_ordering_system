from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )

admin.site.register(Order, OrderAdmin)
admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(ProductAmount)
admin.site.register(IngredientAmount)
admin.site.register(Employee)
admin.site.register(Transaction)