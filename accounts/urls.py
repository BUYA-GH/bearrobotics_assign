from django.urls import path

from accounts.views.card import CardCreateView

urlpatterns = [
    path('card/create/', CardCreateView.as_view(), name='card_create')
]