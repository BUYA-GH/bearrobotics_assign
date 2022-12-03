from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from accounts.models import Card, Account

import random, string

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('cardNum', 'pinNum')
        read_only_fields = ('cardNum', 'pinNum')

class CardCreateSerializer(CardSerializer):
    # both
    cardNum = serializers.CharField(required=False, max_length=16)

    # write-only
    pinNum = serializers.CharField(max_length=4, write_only=True)

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
        Account.objects.create(accountNumber=accountNumber, author=card)
        return card

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields