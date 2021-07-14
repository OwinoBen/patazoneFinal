from django.urls import path
from .views import *

app_name = "carts"
urlpatterns = [
    path('', OrderSummaryView.as_view(), name='home'),
    path(r'^checkout/success/$', checkoutDoneView, name='success'),
    path(r'^shop/$', cartView, name='shop'),
    # path(r'^remove/$', remove_from_cart, name='removecart'),
    # path(r'^checkout/$', checkoutHome, name='checkout'),
    path(r'^update/$', updateCart, name='update'),
    path(r'^quickcheck/(?P<id>)/$', QuickCheck, name='quickcheck'),
    path(r'^productdetails/(?P<id>)/$', productDetails, name='productdetails'),
    path('removed/<int:product_id>', remove_single_item_from_cart, name="removefromcart"),
]