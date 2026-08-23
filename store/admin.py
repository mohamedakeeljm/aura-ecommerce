from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'subtotal']
    
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'email', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'email', 'phone']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'total_price', 'created_at']
    
    fieldsets = [
        ('Order Information', {
            'fields': ['order_number', 'total_price', 'status', 'created_at']
        }),
        ('Customer Details', {
            'fields': ['user', 'customer_name', 'email', 'phone', 'address', 'city']
        }),
    ]
