from django.urls import path
from .views import *

app_name = "carts"
urlpatterns = [
    path('', OrderSummaryView.as_view(), name='home'),
    path('checkout/success/$', checkoutDoneView, name='success'),
    path('shop/$', cartView, name='shop'),
    # path(r'^remove/$', remove_from_cart, name='removecart'),
    # path(r'^checkout/$', checkoutHome, name='checkout'),
    # path('update/<int:product_id>', updateCart, name='update'),
    path('update/', updateCart, name='update'),
    path('^quickcheck/(?P<id>)/$', QuickCheck, name='quickcheck'),
    path('productdetails/<int:id>/<keyword>$', productDetails, name='productdetails'),
    path('removed/<int:product_id>', remove_single_item_from_cart, name="removefromcart"),
]