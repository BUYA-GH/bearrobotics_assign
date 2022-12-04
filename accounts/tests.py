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

    def do_계좌_보기(self, accountNumber):
        res: Response = self.client.post(
            reverse('get_balance'),
            data={
                'accountNumber': accountNumber
            },
            format='json',
        )
        return res

    def do_입금(self, accountNumber, receivedPaid):
        res: Response = self.client.post(
            reverse('deposit'),
            data={
                'accountNumber': accountNumber,
                'receivedPaid': receivedPaid
            },
            format='json',
        )
        return res

    def do_출금(self, accountNumber, receivedPaid):
        res: Response = self.client.post(
            reverse('withdraw'),
            data={
                'accountNumber': accountNumber,
                'receivedPaid': receivedPaid
            },
            format='json',
        )
        return res

    def do_거래_내역_보기(self, accountNumber):
        res: Response = self.client.post(
            reverse('get_transaciton_list'),
            data={
                'accountNumber': accountNumber
            },
            format='json',
        )
        return res

    def test_create_card_account(self):
        res: Response = self.do_카드_계좌_생성(pinnum="1234")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['cardNum']), 16)

    def test_create_card_and_insert_pin_number(self):
        res1: Response = self.do_카드_계좌_생성(pinnum="1234")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(len(res1.data['cardNum']), 16)

        res2: Response = self.do_카드_삽입(pinnum="1234", cardnum=res1.data['cardNum'])
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['cardNum'], res1.data['cardNum'])
        self.assertEqual(res2.data['accountNumber'], res1.data['accountNumber'])
    
    def test_insert_incorrect_pin_number(self):
        res1: Response = self.do_카드_계좌_생성(pinnum="1234")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(len(res1.data['cardNum']), 16)

        res2: Response = self.do_카드_삽입(pinnum="5678", cardnum=res1.data['cardNum'])
        self.assertEqual(res2.status_code, 400)

    def test_insert_card_and_see_balance(self):
        res1: Response = self.do_카드_계좌_생성(pinnum="1234")
        res1: Response = self.do_카드_삽입(pinnum="1234", cardnum=res1.data['cardNum'])

        res2: Response = self.do_계좌_보기(accountNumber=res1.data['accountNumber'])
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['author'], res1.data['cardNum'])
        self.assertEqual(res2.data['accountNumber'], res1.data['accountNumber'])
        self.assertEqual(res2.data['balance'], 0)

    def test_check_deposit_and_withdraw(self):
        res1: Response = self.do_카드_계좌_생성(pinnum="1234")
        res1: Response = self.do_카드_삽입(pinnum="1234", cardnum=res1.data['cardNum'])

        res2: Response = self.do_입금(accountNumber=res1.data['accountNumber'], receivedPaid=30)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['account'], res1.data['accountNumber'])
        self.assertEqual(res2.data['receivedPaid'], 30)
        self.assertEqual(res2.data['is_deposit'], True)
        self.assertEqual(res2.data['balance'], 30)

        res2: Response = self.do_출금(accountNumber=res1.data['accountNumber'], receivedPaid=15)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['account'], res1.data['accountNumber'])
        self.assertEqual(res2.data['receivedPaid'], 15)
        self.assertEqual(res2.data['is_deposit'], False)
        self.assertEqual(res2.data['balance'], 15)

    def test_check_breakdown(self):
        res1: Response = self.do_카드_계좌_생성(pinnum="1234")
        res1: Response = self.do_카드_삽입(pinnum="1234", cardnum=res1.data['cardNum'])
        res2: Response = self.do_입금(accountNumber=res1.data['accountNumber'], receivedPaid=30)
        res2: Response = self.do_입금(accountNumber=res1.data['accountNumber'], receivedPaid=30)
        res2: Response = self.do_출금(accountNumber=res1.data['accountNumber'], receivedPaid=15)

        res3: Response = self.do_거래_내역_보기(accountNumber=res1.data['accountNumber'])
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(len(res3.data), 3)