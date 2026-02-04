from django import forms
from .models import Transaction, Account, Budget, Category, Savings, BankConnection, BankTransaction


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

class BankConnectionForm(forms.ModelForm):
    """Form pentru conectare bănci"""
    class Meta:
        model = BankConnection
        fields = ['bank', 'account_name', 'account_number', 'access_token']
        widgets = {
            'bank': forms.Select(attrs={'class': 'form-control'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume cont (ex: Revolut Privat)'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Număr IBAN (opțional)'}),
            'access_token': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Token API'}),
        }
        help_texts = {
            'bank': 'Selectează banca',
            'access_token': 'Introdu token-ul API. Pentru Revolut: folosește personal token din setări. Pentru BT: folosește token din Open Banking.',
        }


class BankTransactionSyncForm(forms.Form):
    """Form pentru sincronizare tranzacții"""
    days_back = forms.IntegerField(
        initial=30,
        min_value=1,
        max_value=365,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        label='Sincronizează tranzacții din ultimele N zile'
    )
    auto_create_transactions = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Creează automat tranzacții în cont'
    )


class BankTransactionReviewForm(forms.Form):
    """Form pentru revizuire și editare tranzacții din bănci"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Categorie'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Descriere'
    )
    accept = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Acceptă tranzacția'
    )