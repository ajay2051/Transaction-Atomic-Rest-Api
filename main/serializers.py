from rest_framework import serializers

from main.models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'sender_account', 'receiver_account', 'amount']
