from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def seller_check(user):
    if not user.is_seller:
        raise PermissionDenied()
    return True

@user_passes_test(seller_check)
def seller_dashboard(request):
    return render(request, "seller_dashboard.html")