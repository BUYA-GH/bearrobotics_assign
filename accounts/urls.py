from django.urls import path

from accounts.views.card import *

urlpatterns = [
    path('card/create/', CardCreateView.as_view(), name='card_create'),
    path('card/', InsertCardView.as_view(), name='insert_card')
]