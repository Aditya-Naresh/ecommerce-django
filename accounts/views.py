from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Email Verification
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.views.decorators.cache import never_cache
from orders.models import Order, OrderProduct

from addressbook.models import UserAddressBook

import requests

import environ

env = environ.Env()
environ.Env.read_env()


def register(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect("dashboard")
    code = str(kwargs.get("ref_code"))
    try:
        profile = UserProfile.objects.get(code=code)
        request.session["ref_profile"] = profile.id
    except:
        pass
    print(request.session.get_expiry_date)
    if request.method == "POST":
        profile_id = request.session.get("ref_profile")

        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )

            user.phone_number = phone_number
            user.save()
            instance = user

            if profile_id is not None:
                recommended_by_profile = UserProfile.objects.get(id=profile_id)
                registered_user = Account.objects.get(id=instance.id)
                registered_profile = UserProfile.objects.get(user=registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
            else:
                pass
            # User activation
            current_site = "3.22.101.247:8000"
            mail_subject = "Account Activation"

            message = render_to_string(
                "accounts/account_verification_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            messages.success(
                request, "We have set you an email. Please verify your email"
            )

            return redirect("/accounts/login?command=verification&email=" + email)
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            usera = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, "User does not Exist")
            return redirect("login")

        if usera.is_blocked:
            messages.error(request, "User is blocked")
            return redirect("login")

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting the product variations by cart id
                    product_variation = []

                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))

                    # Get cart items from the user to access the product variations
                    cart_item = CartItem.objects.filter(user=user)
                    existing_variations_list = []
                    id = []
                    for item in cart_item:
                        existing_variations = item.variation.all()
                        existing_variations_list.append(list(existing_variations))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in existing_variations_list:
                            index = existing_variations_list.index(pr)
                            item_id = id[index]

                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                return redirect("dashboard")

        else:
            messages.error(request, "Invalid login credentials")
    return render(request, "accounts/login.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations Your account is activated")
        return redirect("login")

    else:
        messages.error(request, "Invalid activation link")
        return redirect("register")


# =========== Dashboard ==================
@login_required(login_url="login")
@never_cache
def dashboard(request):
    orders = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id, is_ordered=True
    )
    site  = env("DOMAIN")
    orders_count = orders.count
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {"orders_count": orders_count, "userprofile": userprofile ,"site" : site}
    return render(request, "accounts/dashboard.html", context)


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password
            current_site = env("DOMAIN")
            mail_subject = "Password Reset"

            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

            messages.success(
                request, "Password reset email has been sent to your email Address"
            )
            return redirect("login")

        else:
            messages.error(request, "Account does not exist")
            return redirect("forgotPassword")

    return render(request, "accounts/forgotPassword.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("resetPassword")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("login")


def resetPassword(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("resetPassword")

    else:
        return render(request, "accounts/resetPassword.html")


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by(
        "-created_at"
    )

    context = {
        "orders": orders,
    }

    return render(request, "dashboard/my_orders.html", context)


@login_required(login_url="login")
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect("edit_profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "userprofile": userprofile,
    }
    return render(request, "dashboard/edit_profile.html", context)


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST["current_password"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, "Password updated successfully")
                return redirect("change_password")
            else:
                messages.error(request, "Please enter Valid current password")
                return redirect("change_password")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("change_password")
    return render(request, "dashboard/change_password.html")


@login_required(login_url="login")
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_detail = OrderProduct.objects.filter(order=order)

    subtotal = sum(item.product_price * item.quantity for item in order_detail)

    context = {"order_detail": order_detail, "order": order, "subtotal": subtotal}
    return render(request, "dashboard/order_detail.html", context)


# =========================== Dashboard Addresses =======================================================


def addressbook(request):
    addresses = UserAddressBook.objects.filter(user=request.user)
    context = {"addresses": addresses}
    return render(request, "dashboard/addressbook.html", context)
