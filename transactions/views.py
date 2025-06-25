from django.shortcuts import render , redirect
from django.http import JsonResponse
from .forms import TransactionForm
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from core.models import Member
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import user_in_group
from django import forms

# Assuming the function is in utils.py
@login_required
@user_in_group('transactions')
def create_transaction(request):
    group = None

    if request.method == 'POST':
        group_id = request.POST.get('group')
        group = get_object_or_404(MemberGroup, id=group_id, members__user=request.user)
        form = TransactionForm(request.POST, group=group)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.initiated_by = Member.objects.get(user=request.user)
            transaction.group = group
            transaction.save()
            form.save_m2m()

            involved = transaction.involved_members.count()
            LedgerEntry.objects.create(
                transaction=transaction,
                group=transaction.group,
                user=transaction.paid_by,
                amount=-1 * transaction.amount,
                description=f"{transaction.transaction_type}: {transaction.description}"
            )

            if involved > 0:
                share = transaction.amount / involved
                for member in transaction.involved_members.all():
                    LedgerEntry.objects.create(
                        transaction=transaction,
                        group=transaction.group,
                        user=member,
                        amount=share,
                        description=f"{transaction.transaction_type}: {transaction.description}"
                    )

            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user, group=None)

    return render(request, 'transactions/create_transaction.html', {'form': form})
def renew_rent():
    today = date.today()
    liabilities = DefaultLiability.objects.filter(due_date__lte=today)

    for liability in liabilities:
        # Create a new transaction for the rent
        Transaction.objects.create(
            paid_by=None,  # No one has paid yet
            initiated_by=liability.user,
            transaction_type="Monthly Rent",
            amount=liability.amount,
            description=f"Rent for {today.strftime('%B %Y')}"
        )
        # Update the due date to the next month
        liability.due_date += timedelta(days=30)  # Adjust for exact month length if needed
        liability.save()

@user_in_group('transactions')
@login_required
def trigger_renew_rent(request):
    renew_rent()
    return JsonResponse({"message": "Rent renewed successfully!"})

def calculate_user_liability(user, group=None):
    from django.db.models import Sum

    # Filter ledger entries by group if provided
    if group:
        ledger_entries = user.ledger_entries.filter(group=group)
    else:
        ledger_entries = user.ledger_entries.all()

    # Calculate total liabilities and payments
    total_liability = ledger_entries.filter(amount__gt=0).aggregate(total=Sum('amount'))['total'] or 0
    total_payments = ledger_entries.filter(amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0

    # Final liability (debit - credit)
    net_liability = total_liability + total_payments 
    print(net_liability) # Payments are negative, so we add them

    return {
        'total_liability': total_liability,  # Total liabilities (debit)
        'total_payments': abs(total_payments),  # Total payments (credit)
        'net_liability': net_liability       # Final liability
    }

@login_required
@user_in_group('transactions')
def group_liabilities_view(request, group_id):
    group = get_object_or_404(MemberGroup, id=group_id)
    members = group.members.all()
    liabilities = []
    transactions= Transaction.objects.filter(group=group).order_by('-date')

    for member in members:
        liability_data = calculate_user_liability(member, group=group)
        liabilities.append({
            'user': member,
            'total_liability': liability_data['total_liability'],
            'total_payments': liability_data['total_payments'],
            'net_liability': liability_data['net_liability'],
        })

    total_group_liability = sum(item['total_liability'] for item in liabilities)
    total_group_payments = sum(item['total_payments'] for item in liabilities)
    other_groups = request.user.member.member_groups.exclude(id=group.id)
    return render(request, 'transactions/group_liabilities.html', {
        'group': group,
        'liabilities': liabilities,
        'total_group_liability': total_group_liability,
        'total_group_payments': total_group_payments,
        'net_group_liability': total_group_liability - total_group_payments,
        'transactions': transactions,
        'other_groups': other_groups,
    })


@user_in_group('transactions')
@login_required
def user_liability_view(request, user_id):
    user = get_object_or_404(Member, id=user_id)
    groups = user.member_groups.all()
    liability_data = calculate_user_liability(user)
    ledger_entries = user.ledger_entries.all().order_by('-transaction__date')
    involved_members_list = [list(entry.transaction.involved_members.all()) for entry in ledger_entries]
    print(involved_members_list)
    return render(request, 'transactions/user_liability.html', {
        'groups': groups,
        'user': user,
        'total_liability': liability_data['total_liability'],
        'total_payments': liability_data['total_payments'],
        'net_liability': liability_data['net_liability'],
        'transactions': ledger_entries,
    })
@login_required
@user_in_group('transactions')
def transaction_list(request):
    transactions = Transaction.objects.all()
    groups = request.user.member.member_groups.all()
    return render(request, 'transactions/transasction_list.html', {'transactions': transactions
                                                                   , 'groups': groups})


@login_required
@user_in_group('transactions')
def make_payment(request, group_id):
    group = get_object_or_404(MemberGroup, id=group_id)
    payer = request.user.member
    members = group.members.exclude(id=payer.id)

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description', 'Payment made')
        recipient = get_object_or_404(Member, id=recipient_id)

        # Create a Payment transaction
        transaction = Transaction.objects.create(
            group=group,
            paid_by=payer,
            amount=amount,
            description=description,
            transaction_type='Payment',
            initiated_by=payer
        )
        transaction.involved_members.set([recipient])  # Must include recipient for proper ledger logic
        transaction.save()

        messages.success(request, f"Payment of {amount} to {recipient.user.username} recorded successfully!")
        return redirect('group_liability', group_id=group.id)

    return render(request, 'transactions/make_payment.html', {
        'group': group,
        'members': members
    })
@login_required
@staff_member_required
@user_in_group('transactions')
def update_transaction(request, transaction_id):
    print("Update transaction view called")
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, initiated_by__user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, group=transaction.group)
        if form.is_valid():
            print("form is valid deleting old ledger entries")
            # Delete old ledger entries linked to this transaction
            LedgerEntry.objects.filter(transaction=transaction).delete()
            print("old ledger entries deleted")

            updated_transaction = form.save(commit=False)
            updated_transaction.save()
            form.save_m2m()

            # Recreate ledger entries
            involved = updated_transaction.involved_members.all()
            share = updated_transaction.amount / involved.count()

            involved = transaction.involved_members.count()
            LedgerEntry.objects.create(
                transaction=transaction,
                group=transaction.group,
                user=transaction.paid_by,
                amount=-1 * transaction.amount,
                description=f"{transaction.transaction_type}: {transaction.description}"
            )

            if involved > 0:
                share = transaction.amount / involved
                for member in transaction.involved_members.all():
                    LedgerEntry.objects.create(
                        transaction=transaction,
                        group=transaction.group,
                        user=member,
                        amount=share,
                        description=f"{transaction.transaction_type}: {transaction.description}"
                    )

            return redirect('transaction_list')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = TransactionForm(instance=transaction, group=transaction.group)
        form.fields['group'].disabled = True  # Make the group field uneditable

    return render(request, 'transactions/update_transaction.html', {'form': form})
@login_required
@user_in_group('transactions')
def get_members(request, group_id):
    group = get_object_or_404(MemberGroup, id=group_id)
    members = group.members.all()

    involved_html = render_to_string(
        'transactions/partial_members.html',
        {'members': members, 'is_paid_by': False},
        request=request
    )
    paid_by_html = render_to_string(
        'transactions/partial_members.html',
        {'members': members, 'is_paid_by': True},
        request=request
    )

    return JsonResponse({'involved_html': involved_html, 'paid_by_html': paid_by_html})