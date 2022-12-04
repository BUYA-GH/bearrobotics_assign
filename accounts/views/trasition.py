from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.serializers.trasition import *

class BalanceView(APIView):
    def get(self, request):
        instance = Account.objects.get(accountNumber=request.data['accountNumber'])
        serializer = AccountSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionListView(APIView):
    def get(self, request):
        queryset = [transact for transact in Transaction.objects.filter(account__accountNumber=request.data['accountNumber']).order_by('-transact_at')]
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

class TransactionBaseView(APIView):
    is_deposit = True

    def post(self, request):
        # is_deposit = serializers.SerializerMethodField()
        # print(request.data)
        serializer = TransactionWorkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_deposit=self.is_deposit)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DepositView(TransactionBaseView):
    is_deposit = True

class WithdrawView(TransactionBaseView):
    is_deposit = False
