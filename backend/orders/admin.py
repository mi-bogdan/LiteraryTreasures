from django.contrib import admin


from .models import Order,OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name","city","status","total_price","payment_id","created_at")
    list_display_links = ("id", "full_name","city")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "order", "quantity")
    list_display_links = ("id", "book", "order", "quantity")


