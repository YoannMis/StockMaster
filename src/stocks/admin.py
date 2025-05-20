from django.contrib import admin

from stocks.models import Warehouse, Product, Stock, StockMovement

admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(StockMovement)
