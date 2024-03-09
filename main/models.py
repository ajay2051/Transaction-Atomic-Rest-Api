from django.db import models


# Create your models here.

class Account(models.Model):
    account_number = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __int__(self):
        return self.account_number


class Transaction(models.Model):
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_payments')
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.amount} from {self.sender_account} to {self.receiver_account}"
