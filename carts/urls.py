from django.urls import path
from .views import cart_home, updateCart,  checkoutDoneView,QuickCheck,productDetails, cartView,OrderSummaryView

app_name = "carts"
urlpatterns = [
    path('', OrderSummaryView.as_view(), name='home'),
    path(r'^checkout/success/$', checkoutDoneView, name='success'),
    path(r'^shop/$', cartView, name='shop'),
    # path(r'^checkout/$', checkoutHome, name='checkout'),
    path(r'^update/$', updateCart, name='update'),
    path(r'^update/$', updateCart, name='update'),
    path(r'^quickcheck/(?P<id>)/$', QuickCheck, name='quickcheck'),
    path(r'^productdetails/(?P<id>)/$', productDetails, name='productdetails'),
]
# r'^emp_detail/(?P<id>\w+)/(?P<mobile_number>\d{10,18})/$'