from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Card, Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ('accountNumber', 'balance', 'author',)
        read_only_fields = ('accountNumber', 'balance', 'author',)

class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.SlugRelatedField(
        read_only=True,
        slug_field='accountNumber'
    )

    class Meta:
        model = Transaction
        fields = ('account', 'receivedPaid', 'is_deposit', 'transact_at',)
        read_only_fields = ('account', 'receivedPaid', 'is_deposit', 'transact_at',)

class TransactionWorkSerializer(TransactionSerializer):
    # read-only : not need to override

    # both
    receivedPaid = serializers.IntegerField()

    # write-only
    accountNumber = serializers.CharField(write_only=True)

    def validate_receivedPaid(self, value):
        if value <= 0:
            raise ValidationError('receivedPaid should be Positive')
        return value

    def create(self, validated_data):
        accountNumber = validated_data.pop('accountNumber')

        account = Account.objects.get(accountNumber=accountNumber)
        account.balance += validated_data['receivedPaid'] * (1 if validated_data['is_deposit'] else -1)
        if account.balance < 0:
            raise ValidationError("Balance cannot be less than zero.")
        account.save()

        validated_data['account'] = account
        transaction = Transaction(**validated_data)
        transaction.save()
        return transaction

    class Meta(TransactionSerializer.Meta):
        fields = TransactionSerializer.Meta.fields + ('accountNumber',)