from django.contrib.auth.models import AbstractUser
from django.db import models

class PaymentManager(models.Manager):
    def create_payment(self, sender, recipient_email, recipient_name, amount, status):
        payment = self.create(
            sender=sender,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            amount=amount,
            status=status
        )
        return payment


class User(AbstractUser):
    username = models.CharField(null=True, max_length=255,default='',unique=False)
    last_name = models.CharField(null=True, max_length=255,default='',unique=False)
    first_name = models.CharField(null=True, max_length=255,default='',unique=False)
    email = models.EmailField(primary_key=True,unique=True)
    name = models.CharField(null=False, max_length=255,default='')
    password = models.CharField(null=False, max_length=255)
    account_balance = models.DecimalField(null=False, max_digits=10, decimal_places=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']

    def __str__(self):
        return f"{self.email}"


class Payment(models.Model):
    # id =models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_payments',db_column='sender')
    recipient_email = models.EmailField(null=False)
    recipient_name = models.CharField(null=False, max_length=255)
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    status = models.CharField(null=False, max_length=255)

    objects = PaymentManager()

    def __str__(self):
        return f"Payment {self.sender} to {self.recipient_email}"
    