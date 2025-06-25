from django.db import models
from core.models import Member

class MemberGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Member, related_name='member_groups')
    def __str__(self):
        return self.name
class LedgerEntry(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, null=True, blank=True, related_name="ledger_entries")
    group = models.ForeignKey(MemberGroup, on_delete=models.CASCADE, related_name="ledger_entries")
    user = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="ledger_entries")
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Positive for liabilities, negative for payments
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} in {self.group.name} on {self.date}"
class Transaction(models.Model):
    group = models.ForeignKey(MemberGroup, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="paid_transactions", limit_choices_to={'member_groups__isnull': False})
    initiated_by = models.ForeignKey(Member, on_delete=models.CASCADE, limit_choices_to={'member_groups__isnull': False}, related_name="initiated_transactions")
    transaction_id = models.AutoField(primary_key=True)
    transaction_type = models.CharField(max_length=50, default='khaja kharcha')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    involved_members = models.ManyToManyField(Member, related_name="involved_transactions", limit_choices_to={'member_groups__isnull': False})
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.pk:
            # Clear existing ledger entries for this transaction
            LedgerEntry.objects.filter(transaction=self).delete()

            involved = self.involved_members.all()
            involved_count = involved.count()

            if self.transaction_type == 'Payment' and involved_count == 1:
                recipient = involved.first()
                # Payer gets negative, recipient gets positive
                LedgerEntry.objects.create(
                    transaction=self,
                    group=self.group,
                    user=self.paid_by,
                    amount=-self.amount,
                    description=f"Payment to {recipient.user.username}: {self.description}"
                )
                LedgerEntry.objects.create(
                    transaction=self,
                    group=self.group,
                    user=recipient,
                    amount=self.amount,
                    description=f"Payment from {self.paid_by.user.username}: {self.description}"
                )
        
    
class DefaultLiability(models.Model):
    group = models.ForeignKey(MemberGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(Member, on_delete=models.CASCADE,  limit_choices_to={'member_groups__isnull': False})
    name = models.CharField(max_length=100 , default="rent")  # e.g., "Rent"
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()  # Tracks when the next rent is due

    def __str__(self):
        return f"{self.name} - {self.amount} for {self.user}"
    
class Payment(models.Model):
    payer = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments_made")
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments_received")
    group = models.ForeignKey(MemberGroup, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.payer} paid {self.recipient} {self.amount} on {self.date}"
    

