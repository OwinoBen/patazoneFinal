import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from address.models import Address
from billing.models import BillingProfile
from django.conf import settings

from carts.views import create_ref_code
from mpesa.views import HOST_USER_EMAIL
from .forms import CheckoutForm, CouponForm, PaymentForm
from .models import Order, ProductPurchase, UserProfile, Payment, OrderItem


class OrderListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        raise Http404


class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'order/library.html'

    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            product_id = request.GET.get('product_id', None)
            if product_id is not None:
                product_id = int(product_id)
                ownership_ids = ProductPurchase.objects.products_by_id(request)
                if product_id in ownership_ids:
                    return JsonResponse({'owner': True})
        raise Http404


def checkoutView(request):
    context = {}
    return render(request, 'checkout.html', context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def saveAddress(request):
    error = ''
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    mobilePhone = request.POST['mobilephone1']
    mobilePhone2 = request.POST['mobilephone2']
    deliveryAddress = request.POST['deliveryAddress']
    state_region = request.POST['state']
    city = request.POST['city']
    set_default_shipping = request.POST.get('set_default_shipping_address')
    if firstname != "" and lastname != '' and mobilePhone != '' and deliveryAddress != '' and state_region != '' and city != '':
        try:
            phone = Address.objects.get(mobile_phone=mobilePhone)
            return render(request, 'checkout.html',
                          {'error': 'Address  with the phone number already exists'})
        except Address.DoesNotExist:
            order = Order.objects.get(user=request.user, ordered=False)
            shipping_address = Address(
                user=request.user,
                firstname=firstname,
                lastname=lastname,
                delivery_address=deliveryAddress,
                region=state_region,
                mobile_phone=mobilePhone,
                mobile=mobilePhone2,
                city=city,
                address_type='S'
            )
            shipping_address.save()
            order.shipping_address = shipping_address
            order.save()
            address_qs = Address.objects.filter(user=request.user, default=True)
            if set_default_shipping:
                if address_qs.exists():
                    return render(request, 'checkout.html', {'error': "A default shipping address is already set"})
                else:
                    shipping_address.default = True
                    shipping_address.save()
        return redirect('checkout:checkout')
    else:
        error = "Please fill in the required shipping address fields"
    context = {'error': error}
    return render(request, 'checkout.html', context)


def payondelivery(request, payment_option):
    return render(request, 'mpesaondelivery.html')


def pay(request, payment_option):
    order = Order.objects.get(user=request.user, ordered=False)
    context = {
        'order': order
    }
    return render(request, 'payment.html', context)


def confirmPayment(request):
    payment_option = request.POST['payment_option']
    print(payment_option)
    if payment_option == 'paynow':
        return redirect('orders:pay', payment_option='paynow')
    elif payment_option == 'payondelivery':
        order = Order.objects.filter(user=request.user, ordered=False)
        try:
            address = Address.objects.get(user=request.user, default=True)
            orderitems = order.cart.all()
            orderitems.update(ordered=True)
            for item in orderitems:
                item.save()
            order.ordered = True
            order.paid_amount = order.get_total()
            order.customerNumber = address.mobile_phone
            order.status = 'Pending'
            order.delivery = 'Customer delivery'
            order.payment_method = 'Mpesa payment'
            order.save()
            subject = 'Patazone marketplace, order placement'
            message = 'You have successfully placed an order with patazone marketplace.\n your order will be ' \
                      'shipped within two days '
            receipient = str(request.user.email)

            send_mail(subject, message, HOST_USER_EMAIL, [receipient], fail_silently=False)

            return redirect('register:orders')
        except Address.DoesNotExist:
            messages.error(request, 'Please Add your shipping Address')
            print('no address found')

            return redirect('checkout:checkout')
    else:
        messages.warning(request, "Invalid payment option selected")
        return redirect('')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            shipping_addres = Address.objects.filter(user=self.request.user, address_type='S', default=True)
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'shipping_addres': shipping_addres,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            # apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        print("incomplete entry")
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('checkout:payment', payment_option='card')
                elif payment_option == 'P':
                    return redirect('checkout:payment', payment_option='paypal')
                elif payment_option == 'M':

                    return redirect('checkout:payment', payment_option='mpesa')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
        return redirect("checkout:checkout")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "checkout.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("checkout:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


def order_pick_from_store(request):
    pickup = request.POST['pickupPhone']
    if request.method == 'POST':
        order = Order.objects.get(user=request.user, ordered=False)
        orderItems = order.cart.all()
        orderItems.update(ordered=True)
        for orderitem in orderItems:
            orderitem.save()
        order.ordered = True
        order.customerNumber = pickup
        order.status = 'Pending'
        order.delivery = 'Pick from store'
        order.save()

        subject = 'Patazone marketplace, order placement'
        message = 'You have successfully placed an order with patazone marketplace.\n your order will be ' \
                  'shipped within two days '
        receipient = str(request.user.email)

        send_mail(subject, message, HOST_USER_EMAIL, [receipient], fail_silently=False)
    return redirect('register:orders')
