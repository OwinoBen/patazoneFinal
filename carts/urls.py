from django.urls import path
from .views import OrderSummaryView, updateCart, checkoutHome, checkoutDoneView,QuickCheck,productDetails, cartView

app_name = "carts"
urlpatterns = [
    path('', OrderSummaryView.as_view(), name='home'),
    path(r'^checkout/success/$', checkoutDoneView, name='success'),
    path(r'^shop/$', cartView, name='shop'),
    path(r'^checkout/$', checkoutHome, name='checkout'),
    path(r'^update/$', updateCart, name='update'),
    path(r'^update/$', updateCart, name='update'),
    path(r'^quickcheck/(?P<id>)/$', QuickCheck, name='quickcheck'),
    path(r'^productdetails/(?P<id>)/$', productDetails, name='productdetails'),
]
# r'^emp_detail/(?P<id>\w+)/(?P<mobile_number>\d{10,18})/$'