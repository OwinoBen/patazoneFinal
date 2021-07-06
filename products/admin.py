from django.contrib import admin
from .models import Product, ProductFile, SlideShow


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'is_digital']
    inlines = [ProductFileInline]

    class Meta:
        model = Product


class SlideShowAdmin(admin.ModelAdmin):
    list_display = ['name', 'file']


admin.site.register(Product, ProductAdmin)
admin.site.register(SlideShow,SlideShowAdmin)
