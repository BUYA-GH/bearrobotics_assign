from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Card, Account, Transition

class AccountSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ('accountNumber', 'balance', 'author',)
        read_only_fields = ('accountNumber', 'balance', 'author',)

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transition
#         fields = ('account', 'receivedPaid', 'transact_at',)
#         read_only_fields = ('account', 'receivedPaid', 'transact_at',)

# class TransactionWorkSerializer(TransactionSerializer):
#     pass