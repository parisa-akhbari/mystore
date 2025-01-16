from django.contrib import admin
from .models import NewShippingAddress,Order,OrderItem

admin.site.register(NewShippingAddress)
#admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.TabularInline):
    model=OrderItem
    extra=1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemInLine]
    