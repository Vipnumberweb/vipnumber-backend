import typing
from django.contrib import messages
from allauth.account.adapter import DefaultAccountAdapter
from .models import VN_User


class VN_AccountAdapter(DefaultAccountAdapter):
    def set_phone(self, user, phone: str, verified: bool):
        user.phone = phone
        user.phone_verified = verified
        user.save(update_fields=["phone", "phone_verified"])

    def get_phone(self, user) -> typing.Optional[typing.Tuple[str, bool]]:
        if user.phone:
            return user.phone, user.phone_verified
        return None
    
    def set_phone_verified(self, user, phone):
        self.set_phone(user, phone, True)

    def send_verification_code_sms(self, user, phone: str, code: str, **kwargs):
        messages.add_message(
            self.request,
            messages.WARNING,
            f"⚠️ SMS demo stub: assume code {code} was sent to {phone}.",
        )

    def send_unknown_account_sms(self, phone: str, **kwargs):
        messages.add_message(
            self.request,
            messages.WARNING,
            f"⚠️ SMS demo stub: Enumeration prevention: texted {phone} informing no account exists.",
        )

    def get_user_by_phone(self, phone):
        return VN_User.objects.filter(phone=phone).order_by("-phone_verified").first()
