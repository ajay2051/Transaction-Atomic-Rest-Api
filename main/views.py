from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from main.models import Account
from main.serializers import TransactionSerializer


class PaymentView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = TransactionSerializer.Meta.model.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        sender_account_no = serializer.validated_data.get('sender_account')
        receiver_account_no = serializer.validated_data.get('receiver_account')
        amount = serializer.validated_data.get('amount')

        sender_account_object = Account.objects.get(account_number=sender_account_no)
        print("sender_account_object", sender_account_object)
        sender_account_number = sender_account_object.account_number
        print("sender_account_number", sender_account_number)
        receiver_account_object = Account.objects.get(account_number=receiver_account_no)
        print("receiver_account_object", receiver_account_object)

        receiver_account_number = receiver_account_object.account_number
        print("receiver_account_number", receiver_account_number)

        try:
            if sender_account_number and receiver_account_number:
                with transaction.atomic():
                    if amount > sender_account_object.balance or receiver_account_number == sender_account_number:
                        return Response({"message": "Invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
                    sender_account_object.balance -= amount
                    sender_account_object.save()
                    receiver_account_object.balance += amount
                    receiver_account_object.save()
                    self.perform_create(serializer)
                    return Response({"data": serializer.data, "message": "Transaction Successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": print(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()
