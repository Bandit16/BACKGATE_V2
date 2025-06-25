from django import forms
from .models import Transaction, Member , MemberGroup

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['paid_by', 'group', 'involved_members', 'transaction_type', 'amount', 'description']
        widgets = {
            'involved_members': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = "Select a group"
        self.fields['group'].initial = None  # Important to clear default selection
        
        if group:
            self.fields['involved_members'].queryset = group.members.all()
            self.fields['paid_by'].queryset = group.members.all()  # Limit paid_by as well
        else:
            self.fields['involved_members'].queryset = Member.objects.none()
            self.fields['paid_by'].queryset = Member.objects.none()

    def clean_transaction_type(self):
        transaction_type = self.cleaned_data.get('transaction_type')
        print(f"DEBUG: transaction_type = {transaction_type}")  # Debug statement

        if transaction_type == "Payment":
            raise forms.ValidationError("You cannot select 'Payment' as the transaction type.")
        return transaction_type