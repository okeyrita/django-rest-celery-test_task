from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Wallets
from django.contrib.auth.models import User


@login_required
def user_wallets(request):
    '''
    Show user data of wallets and available opportunities.
    '''
    user_data = Wallets.objects.get(user=request.user)
    name_user = str(request.user.username)

    return render(request, 'wallet/detail_wallet.html',
                  {'user_data': user_data,
                   'name': name_user})


@login_required
def convert_money(request):
    '''
    Convert user money inside account.
    '''
    if request.method == 'POST':
        data = request.POST
        from_currency = data.get('from')
        to_currency = data.get('to')
        amount_money = float(data.get('amount'))
        
        # Здесь надо будет сделать конвертацию  и ошибку 



    user_data = Wallets.objects.get(user=request.user)
    name_user = str(request.user.username)
    return render(request, 'wallet/convert.html',
                  {'user_data': user_data,
                   'name': name_user
                   })


@login_required
def transfer_money(request):
    '''
    Transfer money to another account.
    '''


@login_required
def top_up_account(request):
    '''
    Top up an account.
    '''


@login_required
def withdraw_money(request, user_id):
    '''
    Withdraw money from the system.
    '''
