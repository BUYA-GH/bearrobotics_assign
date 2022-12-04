from django.contrib.auth.hashers import make_password, check_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Card, Account

import random, string

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('cardNum', 'pinNum')
        read_only_fields = ('cardNum', 'pinNum')

class CardCreateSerializer(CardSerializer):
    accountNumber = serializers.SerializerMethodField()

    # both
    cardNum = serializers.CharField(required=False, max_length=16)

    # write-only
    pinNum = serializers.CharField(max_length=4, write_only=True)

    def get_accountNumber(self, obj):
        return self.context['accountNumber']

    def auto_create_cardNum(self):
        rndCardNum = ""
        for _ in range(16):
            rndCardNum += random.choice(string.digits)
        return rndCardNum

    def auto_create_accountNumber(self):
        rndAccountNumber = "110-"
        for _ in range(3):
            rndAccountNumber += random.choice(string.digits)
        rndAccountNumber += "-"
        for _ in range(6):
            rndAccountNumber += random.choice(string.digits)
        return rndAccountNumber

    def hash_pinnum(self, raw_pinnum):
        return make_password(raw_pinnum)

    def create(self, validated_data):
        if not validated_data.get('cardNum', None):
            validated_data['cardNum'] = self.auto_create_cardNum()
        validated_data['pinNum'] = self.hash_pinnum(validated_data['pinNum'])

        card, created = Card.objects.get_or_create(defaults=validated_data, cardNum=validated_data['cardNum'])

        while not created:
            validated_data['cardNum'] = self.auto_create_cardNum()
            card, created = Card.objects.get_or_create(defaults=validated_data, cardNum=validated_data['cardNum'])
        
        accountNumber = self.auto_create_accountNumber()
        account, created = Account.objects.get_or_create(accountNumber=accountNumber, author=card)

        while not created:
            accountNumber = self.auto_create_accountNumber()
            account, created = Account.objects.get_or_create(accountNumber=accountNumber, author=card)

        self.context['accountNumber'] = accountNumber
        return card

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields + ('accountNumber', )

class InsertCardSerializer(CardSerializer):
    # read_only
    accountNumber = serializers.SerializerMethodField()

    # both
    cardNum = serializers.CharField(required=False, max_length=16)

    # write-only
    pinNum = serializers.CharField(max_length=4, required=True, write_only=True)

    def get_accountNumber(self, obj):
        account = Account.objects.get(author__cardNum=obj['cardNum'])
        return account.accountNumber

    def validate(self, data):
        raw_pinNum = data['pinNum']
        card = Card.objects.get(cardNum=data['cardNum'])

        if not check_password(raw_pinNum, card.pinNum):
            raise ValidationError('pinNum is incorrect')
        
        return data

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields + ('accountNumber', )
        