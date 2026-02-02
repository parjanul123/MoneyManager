from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Account, Transaction, Category, Budget, Savings, UserProfile
from .forms import (
    TransactionForm, AccountForm, BudgetForm, 
    SavingsForm, FilterTransactionForm
)


@login_required
def profile(request):
    """Pagina profil utilizator cu date de Discord"""
    return render(request, 'finance/profile.html')


@login_required
def dashboard(request):
    """Pagina principală - Dashboard cu statistici generale"""
    user = request.user
    
    # Conturi
    accounts = user.accounts.all()
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
    
    # Tranzacții din ultima lună
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    recent_transactions = user.transactions.filter(
        date__gte=thirty_days_ago
    ).order_by('-date')[:10]
    
    # Statistici venituri vs cheltuieli (luna curentă)
    month_start = today.replace(day=1)
    month_transactions = user.transactions.filter(date__gte=month_start)
    
    total_expenses = month_transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = month_transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Bugete
    current_month = today.replace(day=1)
    budgets = user.budgets.filter(month=current_month)
    
    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'net_income': total_income - total_expenses,
        'budgets': budgets,
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def account_list(request):
    """Listă cu conturile utilizatorului"""
    accounts = request.user.accounts.all()
    context = {'accounts': accounts}
    return render(request, 'finance/account_list.html', context)


@login_required
def account_detail(request, pk):
    """Detalii pentru un anumit cont"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    transactions = account.transactions.all().order_by('-date')[:20]
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'finance/account_detail.html', context)


@login_required
def account_create(request):
    """Creare cont nou"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('finance:account_list')
    else:
        form = AccountForm()
    
    context = {'form': form}
    return render(request, 'finance/account_form.html', context)


@login_required
def account_edit(request, pk):
    """Editare cont"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('finance:account_detail', pk=account.pk)
    else:
        form = AccountForm(instance=account)
    
    context = {'form': form, 'account': account}
    return render(request, 'finance/account_form.html', context)


@login_required
def account_delete(request, pk):
    """Ștergere cont"""
    account = get_object_or_404(Account, pk=pk, user=request.user)
    
    if request.method == 'POST':
        account.delete()
        return redirect('finance:account_list')
    
    context = {'account': account}
    return render(request, 'finance/confirm_delete.html', context)


@login_required
def transaction_list(request):
    """Listă cu tranzacțiile utilizatorului"""
    transactions = request.user.transactions.all()
    form = FilterTransactionForm()
    
    # Filtrare
    if request.GET:
        form = FilterTransactionForm(request.GET)
        
        account = request.GET.get('account')
        category = request.GET.get('category')
        type_filter = request.GET.get('type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if account:
            transactions = transactions.filter(account_id=account)
        if category:
            transactions = transactions.filter(category_id=category)
        if type_filter:
            transactions = transactions.filter(type=type_filter)
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
    
    transactions = transactions.order_by('-date')
    
    context = {
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'finance/transaction_list.html', context)


@login_required
def transaction_create(request):
    """Creare tranzacție nouă"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            
            # Actualizează soldul contului
            account = transaction.account
            if transaction.type == 'expense':
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount
            account.save()
            
            transaction.save()
            return redirect('finance:transaction_list')
    else:
        form = TransactionForm()
        form.fields['account'].queryset = request.user.accounts.all()
    
    context = {'form': form}
    return render(request, 'finance/transaction_form.html', context)


@login_required
def transaction_edit(request, pk):
    """Editare tranzacție"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    old_amount = transaction.amount
    old_type = transaction.type
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            
            # Actualizează soldul dacă s-a schimbat suma sau tipul
            account = transaction.account
            if old_type != transaction.type or old_amount != transaction.amount:
                # Revert old transaction
                if old_type == 'expense':
                    account.balance += old_amount
                else:
                    account.balance -= old_amount
                
                # Apply new transaction
                if transaction.type == 'expense':
                    account.balance -= transaction.amount
                else:
                    account.balance += transaction.amount
                
                account.save()
            
            return redirect('finance:transaction_list')
    else:
        form = TransactionForm(instance=transaction)
        form.fields['account'].queryset = request.user.accounts.all()
    
    context = {'form': form, 'transaction': transaction}
    return render(request, 'finance/transaction_form.html', context)


@login_required
def transaction_delete(request, pk):
    """Ștergere tranzacție"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Revert transaction from account balance
        account = transaction.account
        if transaction.type == 'expense':
            account.balance += transaction.amount
        else:
            account.balance -= transaction.amount
        account.save()
        
        transaction.delete()
        return redirect('finance:transaction_list')
    
    context = {'transaction': transaction}
    return render(request, 'finance/confirm_delete.html', context)


@login_required
def budget_list(request):
    """Listă cu bugetele utilizatorului"""
    budgets = request.user.budgets.all()
    
    # Calcul cheltuieli vs buget
    for budget in budgets:
        spent = request.user.transactions.filter(
            category=budget.category,
            type='expense',
            date__year=budget.month.year,
            date__month=budget.month.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        budget.spent = spent
        budget.remaining = budget.amount - spent
        budget.percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
    
    context = {'budgets': budgets}
    return render(request, 'finance/budget_list.html', context)


@login_required
def budget_create(request):
    """Creare buget nou"""
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('finance:budget_list')
    else:
        form = BudgetForm()
        form.fields['category'].queryset = Category.objects.filter(type='expense')
    
    context = {'form': form}
    return render(request, 'finance/budget_form.html', context)


@login_required
def budget_delete(request, pk):
    """Ștergere buget"""
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        budget.delete()
        return redirect('finance:budget_list')
    
    context = {'budget': budget}
    return render(request, 'finance/confirm_delete.html', context)


@login_required
def savings_list(request):
    """Listă cu obiectivele de economii"""
    savings = request.user.savings_goals.all()
    
    context = {'savings': savings}
    return render(request, 'finance/savings_list.html', context)


@login_required
def savings_create(request):
    """Creare obiectiv de economii nou"""
    if request.method == 'POST':
        form = SavingsForm(request.POST)
        if form.is_valid():
            savings = form.save(commit=False)
            savings.user = request.user
            savings.save()
            return redirect('finance:savings_list')
    else:
        form = SavingsForm()
    
    context = {'form': form}
    return render(request, 'finance/savings_form.html', context)


@login_required
def savings_edit(request, pk):
    """Editare obiectiv de economii"""
    savings = get_object_or_404(Savings, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = SavingsForm(request.POST, instance=savings)
        if form.is_valid():
            form.save()
            return redirect('finance:savings_list')
    else:
        form = SavingsForm(instance=savings)
    
    context = {'form': form, 'savings': savings}
    return render(request, 'finance/savings_form.html', context)


@login_required
def savings_delete(request, pk):
    """Ștergere obiectiv de economii"""
    savings = get_object_or_404(Savings, pk=pk, user=request.user)
    
    if request.method == 'POST':
        savings.delete()
        return redirect('finance:savings_list')
    
    context = {'savings': savings}
    return render(request, 'finance/confirm_delete.html', context)


@login_required
def reports(request):
    """Rapoarte și analize"""
    user = request.user
    today = timezone.now().date()
    
    # Cheltuieli și venituri pe categorii (luna curentă)
    month_start = today.replace(day=1)
    month_transactions = user.transactions.filter(date__gte=month_start)
    
    expense_by_category = {}
    income_by_category = {}
    
    for category in Category.objects.all():
        expenses = month_transactions.filter(
            category=category,
            type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        income = month_transactions.filter(
            category=category,
            type='income'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        if expenses > 0:
            expense_by_category[category.name] = float(expenses)
        if income > 0:
            income_by_category[category.name] = float(income)
    
    context = {
        'expense_by_category': expense_by_category,
        'income_by_category': income_by_category,
    }
    return render(request, 'finance/reports.html', context)
