from django.urls import path

# from accounts.views.card import *
from accounts.views import *

urlpatterns = [
    path('card/create/', CardCreateView.as_view(), name='card_create'),
    path('card/', InsertCardView.as_view(), name='insert_card'),

    path('trasition/balance/', BalanceView.as_view(), name='get_balance'),
    path('trasition/deposit/', DepositView.as_view(), name='deposit'),
    path('trasition/withdraw/', WithdrawView.as_view(), name='withdraw')
]