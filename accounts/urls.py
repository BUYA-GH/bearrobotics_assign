from django.urls import path

# from accounts.views.card import *
from accounts.views import *

urlpatterns = [
    path('card/create/', CardCreateView.as_view(), name='card_create'),
    path('card/', InsertCardView.as_view(), name='insert_card'),

    path('transaction/balance/', BalanceView.as_view(), name='get_balance'),
    path('transaction/list/', TransactionListView.as_view(), name='get_transaciton_list'),
    path('transaction/deposit/', DepositView.as_view(), name='deposit'),
    path('transaction/withdraw/', WithdrawView.as_view(), name='withdraw')
]