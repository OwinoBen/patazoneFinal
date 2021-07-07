import uuid
import base64

from django.conf import settings
import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

# from address.forms import AddressCheckoutForm
from address.models import Address

from billing.models import BillingProfile
from mpesa.views import HOST_USER_EMAIL
from orders.models import Order
from products.models import Product
from .models import Cart
from orders.models import OrderItem


# Create your views here.

def create_ref_code():
    # return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    # return base64.urlsafe_b64encode(uuid.uuid1().bytes.encode("base64").rstrip())[:25]
    # return str(random.randint(1000000000, 9999999999))
    return str(random.randint(1000, 9999))


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.name,
        "price": x.price,
    }
        for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart = {"cart_obj": cart_obj}
    return render(request, 'cart.html', cart)


def cartView(request):
    shopList = Product.objects.all()
    objects = Cart.objects.all()
    onsale = Product.objects.onSaleDeals()
    context = {'shopList': shopList,
               'onsale': onsale,
               'objects': objects,
               }
    return render(request, 'shop.html', context)


def QuickCheck(request, id):
    check = None
    id = int(id)
    quickCheck = Product.objects.filter(id=id)
    check = quickCheck[0]
    context = {'check': check}
    return render(request, 'shop.html', context)


def productDetails(request, id):
    prod = None
    id = int(id)
    productdetail = Product.objects.filter(id=id)
    if len(productdetail) > 0:
        prod = productdetail[0]
    else:
        prod = None
    context = {'prod': prod}
    return render(request, 'product_details.html', context)


@login_required
def updateCart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    order_item, created = OrderItem.objects.get_or_create(product=product, user=request.user, ordered=False)
    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect("cart:home")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.cart.filter(product__id=product.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{product.title} Quantity successfully updated")
            return redirect("cart:shop")
        else:
            order.cart.add(order_item)
            messages.info(request, f"{product.title} was added in your cart")
            return redirect("cart:shop")
    else:
        updated = timezone.now()
        odr = "ORD"
        order_id = (odr + create_ref_code())
        order = Order.objects.create(user=request.user, updated=updated, order_id=order_id)
        order.cart.add(order_item)
        messages.info(request, f"{product.title} item was added in your cart")
        subject = 'Order submitted successfully (Patazone marketplace)'
        message = 'Your order 46246184414028 has been submitted successfully. Kindly pay within the timelime for ' \
                  'quick dispatch.\n Delivery period varies from Patazome marketplace/Local Seller/Global taking 1-5, ' \
                  '8-15, ' \
                  '10-25 working days respectively. '
        receipient = str(request.user.email)

        send_mail(subject, message, HOST_USER_EMAIL, [receipient], fail_silently=False)

        if product_obj in cart_obj.products.all():
            sku = "PRUD"
            sku_d = (sku + create_ref_code())
            cart_obj.quantity += 1
            cart_obj.save()
            # cart_obj.products.remove(product_obj)
            print(sku_d)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("Ajax request")
            jason_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(jason_data, status=200)
    return redirect("cart:shop")


# @login_required
def add_to_cart(request):
    product = get_object_or_404(Product)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, status='created')
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:update")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    print(product_id)
    product = get_object_or_404(Product, id=product_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.cart.filter(product__id=product.id).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.cart.remove(order_item)
            order_item.delete()
            messages.info(request, f"{product.title} was removed from your cart.")
            return redirect("cart:home")
        else:
            messages.info(request, f"{product.title}This item was not in your cart")
            return redirect("cart:shop")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:shop")


@login_required
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:home")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


# def get_coupon(request, code):
#     try:
#         coupon = Coupon.objects.get(code=code)
#         return coupon
#     except ObjectDoesNotExist:
#         messages.info(request, "This coupon does not exist")
#         return redirect("core:checkout")

# def checkoutHome(request):
#     cart_obj, cart_created = Cart.objects.new_or_get(request)
#     order_obj = None
#     if cart_created or cart_obj.products.count() == 0:
#         return redirect("cart:home")
#
#     login_form = LoginForm(request=request)
#     guest_form = GuestForm(request=request)
#     address_form = AddressCheckoutForm()
#     billing_address_id = request.session.get("billing_address_id", None)
#
#     shipping_address_required = not cart_obj.is_digital
#
#     shipping_address_id = request.session.get("shipping_address_id", None)
#
#     billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
#     address_qs = None
#     has_card = False
#
#     if billing_profile is not None:
#         if request.user.is_authenticated():
#             address_qs = Address.objects.filter(billing_profile=billing_profile)
#         order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
#
#         if shipping_address_id:
#             order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
#             del request.session["shipping_address_id"]
#
#         if billing_address_id:
#             order_obj.billing_address_id = Address.objects.get(id=billing_address_id)
#             del request.session["billing_address_id"]
#
#         if billing_address_id or shipping_address_id:
#             order_obj.save()
#
#     if request.method == "POST":
#         #         CHECKING IF ORDER IS DONE
#         is_prepared = order_obj.check_done()
#         if is_prepared:
#             did_charge, crg_msg = billing_profile.charge(order_obj)
#             if did_charge:
#                 order_obj.mark_paid()
#                 request.session['cart_items'] = 0
#                 del request.session['cart_id']
#                 if not billing_profile.user:
#                     billing_profile.setcards_inactive()
#                 return redirect("cart:success")
#             else:
#                 return redirect("cart:checkout")
#
#     context = {
#         "objects": order_obj,
#         "billing_profile": billing_profile,
#         "login_form": login_form,
#         "guest_form": guest_form,
#         "address_form": address_form,
#         "address_qs": address_qs,
#         "has_card": has_card,
#         "shipping_address_required": shipping_address_required
#     }
#     return render(request, 'cart.html', context)
#

def checkoutDoneView(request):
    return render(request, 'cart.html', {})


class OrderSummaryView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                context = {
                    'object': order
                }
                return render(self.request, 'cart.html', context)
            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect("/")
        else:
            return redirect("register:login")


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{product.name} quantity was updated.")
            return redirect("cart:home")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart:home")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart:home")


# @login_required
def remove_from_cart2(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


# @login_required
def remove_single_item_from_cart(request, slug):
    # product_id =
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

# def get_coupon(request, code):
#     try:
#         coupon = Coupon.objects.get(code=code)
#         return coupon
#     except ObjectDoesNotExist:
#         messages.info(request, "This coupon does not exist")
#         return redirect("core:checkout")
#
#
# class AddCouponView(View):
#     def post(self, *args, **kwargs):
#         form = CouponForm(self.request.POST or None)
#         if form.is_valid():
#             try:
#                 code = form.cleaned_data.get('code')
#                 order = Order.objects.get(
#                     user=self.request.user, ordered=False)
#                 order.coupon = get_coupon(self.request, code)
#                 order.save()
#                 messages.success(self.request, "Successfully added coupon")
#                 return redirect("core:checkout")
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "You do not have an active order")
#                 return redirect("core:checkout")


# class RequestRefundView(View):
#     def get(self, *args, **kwargs):
#         form = RefundForm()
#         context = {
#             'form': form
#         }
#         return render(self.request, "request_refund.html", context)
#
#     def post(self, *args, **kwargs):
#         form = RefundForm(self.request.POST)
#         if form.is_valid():
#             ref_code = form.cleaned_data.get('ref_code')
#             message = form.cleaned_data.get('message')
#             email = form.cleaned_data.get('email')
#             # edit the order
#             try:
#                 order = Order.objects.get(ref_code=ref_code)
#                 order.refund_requested = True
#                 order.save()
#
#                 # store the refund
#                 refund = Refund()
#                 refund.order = order
#                 refund.reason = message
#                 refund.email = email
#                 refund.save()
#
#                 messages.info(self.request, "Your request was received.")
#                 return redirect("core:request-refund")
#
#             except ObjectDoesNotExist:
#                 messages.info(self.request, "This order does not exist.")
#                 return redirect("core:request-refund"
