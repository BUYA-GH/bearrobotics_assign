# from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.response import Response
from test_plus import TestCase

class ATMTestCase(TestCase):
    client_class = APIClient

    def do_카드_계좌_생성(self, pinnum):
        res: Response = self.client.post(
            reverse('card_create'),
            data={
                "pinNum": pinnum
            },
            format='json'
        )
        return res

    def do_카드_삽입(self, pinnum, cardnum):
        res: Response = self.client.post(
            reverse('insert_card'),
            data={
                'pinNum': pinnum,
                'cardNum': cardnum
            },
            format='json',
        )
        return res

    def test_create_card_account(self):
        res: Response = self.do_카드_계좌_생성(pinnum="9443")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['cardNum']), 16)

    def test_create_card_and_insert_pin_number(self):
        res1: Response = self.do_카드_계좌_생성(pinnum="9443")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(len(res1.data['cardNum']), 16)

        res2: Response = self.do_카드_삽입(pinnum="9443", cardnum=res1.data['cardNum'])
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['cardNum'], res1.data['cardNum'])
        self.assertEqual(res2.data['accountNumber'], res1.data['accountNumber'])