from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import EmailActivation, GuestEmail

User = get_user_model()


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            message = """Email does not exist, would you like to <a href="{link}">register</a>""".format(
                link=register_link)
            raise forms.ValidationError(mark_safe(message))
        return email


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # save the passwords in hashed format/ encrypted format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
    fullname = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['last_name']


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    model = User
    fields = ('first_name', 'last_name', 'email', 'password', 'is-active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class GuestForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = ['email']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse("account:resend-activation")
                reconfirming_msg = """Go to <a href='{resend_link}'>resend confirmation email</a>.""".format(
                    resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    message1 = "please check your email to confirm your account or" + reconfirming_msg.lower()
                    raise forms.ValidationError(mark_safe(message1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    message2 = "Email not confirmed." + reconfirming_msg
                    raise forms.ValidationError(mark_safe(message2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Login Credentials")
        login(request, user)
        self.user = user
        return data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'email')
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two passwords does not match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            user.save()
        return user


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

        # def clean_email(self):
        #     email = self.cleaned_data['email'].lower()
        #     try:
        #         account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        #     except User.DoesNotExist:
        #         return email
        #     raise forms.ValidationError('Email "%s" is already in use.' % account)

        def clean_first_name(self):
            first_name = self.cleaned_data['first_name']
            try:
                account = User.objects.exclude(pk=self.instance.pk).get(first_name=first_name)
            except User.DoesNotExist:
                return first_name
            raise forms.ValidationError('User "%s" is already in use.' % first_name)

        def clean_last_name(self):
            last_name = self.cleaned_data['last_name']
            try:
                account = User.objects.exclude(pk=self.instance.pk).get(last_name=last_name)
            except User.DoesNotExist:
                return last_name
            raise forms.ValidationError('User "%s" is already in use.' % last_name)

        def save(self, commit=True):
            account = super(AccountUpdateForm, self).save(commit=False)
            account.first_name = self.cleaned_data['first_name']
            account.last_name = self.cleaned_data['last_name']

            if commit:
                account.save()
                return account
