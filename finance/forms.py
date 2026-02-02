from django import forms
from .models import Transaction, Account, Budget, Category, Savings


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'type', 'amount', 'description', 'date']
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'type', 'balance', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ['name', 'target_amount', 'current_amount', 'deadline', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FilterTransactionForm(forms.Form):
    """Form pentru filtrarea tranzacțiilor"""
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type = forms.ChoiceField(
        choices=[('', '--- Toate ---'), ('expense', 'Cheltuieli'), ('income', 'Venituri')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
