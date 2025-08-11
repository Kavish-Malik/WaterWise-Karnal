# members/adapter.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # ✅ Allow signup only if email is present
        return bool(sociallogin.account.extra_data.get('email'))

    def pre_social_login(self, request, sociallogin):
        # ✅ If already logged in, skip
        if request.user.is_authenticated:
            return

        # ✅ Auto-login if user exists with same email
        email = sociallogin.account.extra_data.get('email')
        if email:
            from allauth.account.utils import perform_login
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                perform_login(request, user, email_verification='optional')
            except User.DoesNotExist:
                pass
