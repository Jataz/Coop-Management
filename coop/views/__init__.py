from .users.login import signup,signin,user_logout_view
from .users.otp import verify_email,resend_otp

from .dashboard import index
from .loan import loan_transactions,loan_application,loan_apply,loan_payment,loan_details,confirm_loan,repay_loan,loan_outstanding
from .subscriptions import subscriptions_transactions,subscriptions_payment
from .shareCapital import share_transactions,share_payment
from .profile import user_profile,edit_profile,change_password