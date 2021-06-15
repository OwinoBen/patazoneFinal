from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from address.forms import AddressCheckoutForm
from address.models import Address

from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart


# Create your views here.
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
    context = {}
    return render(request, 'cart.html', context)


def QuickCheck(request, id):
    check = None
    id = int(id)
    quickCheck = Product.objects.filter(id=id)
    if len(check) > 0:
        check = quickCheck[0]
    else:
        check = None
    context = {'check': check}
    return render(request, 'shop.html,', context)


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


def updateCart(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
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
    return redirect("cart:home")


def checkoutHome(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressCheckoutForm()
    billing_address_id = request.session.get("billing_address_id", None)

    shipping_address_required = not cart_obj.is_digital

    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False

    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]

        if billing_address_id:
            order_obj.billing_address_id = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]

        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == "POST":
        #         CHECKING IF ORDER IS DONE
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.setcards_inactive()
                return redirect("cart:success")
            else:
                return redirect("cart:checkout")

    context = {
        "objects": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "shipping_address_required": shipping_address_required
    }
    return render(request, 'cart.html', context)


def checkoutDoneView(request):
    return render(request, 'cart.html', {})
