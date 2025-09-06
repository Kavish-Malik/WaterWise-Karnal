# members/adapter.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        # Only allow signup if email exists
        return bool(sociallogin.account.extra_data.get('email'))

    def pre_social_login(self, request, sociallogin):
        """
        Connect social account to existing user if email matches.
        Do NOT call perform_login here to avoid redirect loops.
        """
        if request.user.is_authenticated:
            return  # Already logged in, nothing to do

        email = sociallogin.account.extra_data.get('email')
        if not email:
            return

        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            # Connect the social account to existing user
            sociallogin.connect(request, user)
            # Allauth will handle login automatically
        except User.DoesNotExist:
            pass
