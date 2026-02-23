from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from account.forms import RegisterForm
from django.contrib import messages
from account.utils import sent_activation_email, send_password_reset_email
from account.models import User
from django.contrib.auth import get_user_model, authenticate,login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from account.forms import StyledSetPasswordForm as SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


# Create your views here.
User =  get_user_model()

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method== 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            sent_activation_email(request, user)
            messages.success(request,'Please check your email for activate your account.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        if user.is_active:
            messages.info(request,'Your account is already activated. Please log in.')
            return redirect('login')
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your account has been activated successfully! You can now log in.')
        return redirect('login')
    else:
        messages.error(request,'Activation link is invalid!')
        return redirect('home')

def resend_email(request):
    if request.method =='POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request, 'Your acccount is already activated. Please log in.')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('resend_email')
        
        sent_activation_email(request, user)
        messages.success(request, 'A new activation email has been sent. Please check your inbox.')
        return redirect('login')
    return render(request,'resend_email.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        else:
            return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        if not user.is_active:
            messages.error(request, 'Your account is In-Active. Please Activate your account first.')
            return redirect('resend_email')
        if user is not None:
            login(request, user)
            if user.is_seller:
                return redirect('seller_dashboard')
            elif user.is_customer:
                return redirect('customer_dashboard')
            else:
                return redirect('home')

    return render(request,'login.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Your password has been changed successfully.')
            return redirect('account_details')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'] 
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
                return redirect('password_reset')
            
            send_password_reset_email(request, user)
            return redirect('reset_password_done')
    else:
        form = PasswordResetForm()
        
    return render(request,'reset_password.html')

def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
        
        if not default_token_generator.check_token(user, token):
            messages.error(request,'This link is expired or invalid. Please request a new password reset.')
            return redirect('reset_password')
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'reset_password_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request,'Invalid password reset link. Please request a new one.')
        return redirect('reset_password')

def reset_password_done(request):
    return render(request,'reset_password_done.html')

def account_details(request):
    return render(request,'account_details.html')