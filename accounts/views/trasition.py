from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.serializers.trasition import *

class BalanceView(APIView):
    def get(self, request):
        instance = Account.objects.get(accountNumber=request.data['accountNumber'])
        serializer = AccountSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class TransitionBaseView(APIView):
#     is_deposit = 1

#     def post(self, request):
#         serializer = TransactionWorkSerializer(request.data, context={'is_deposit': self.is_deposit})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class DepositView(TransitionBaseView):
#     is_deposit = 1

# class WithdrawView(TransitionBaseView):
#     is_deposit = -1
