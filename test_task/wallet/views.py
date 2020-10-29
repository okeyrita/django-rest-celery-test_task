from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers

from django.contrib.auth.models import User
from .models import Wallets
import json

RATE_DATA_PATH = 'wallet/data/currency.json'


def return_todays_rate():
    with open(RATE_DATA_PATH, 'r', encoding='utf-8') as f:
        data_rate = json.load(f)
    return data_rate


@login_required
def user_wallets(request):
    '''
    Show user data of wallets and available opportunities.
    '''
    user_data = Wallets.objects.get(user=request.user)
    name_user = str(request.user.username)
    data_rate = return_todays_rate()

    return render(request, 'wallet/detail_wallet.html',
                  {'user_data': user_data,
                   'name': name_user,
                   'rate_eur': data_rate.get('EUR'),
                   'rate_usd': data_rate.get('USD'),
                   })


@login_required
def convert_money(request):
    '''
    Convert user money inside account.
    '''
    data_rate = return_todays_rate()
    user_data = Wallets.objects.get(user=request.user)
    error = ''

    if request.method == 'POST':
        data = request.POST
        from_currency = data.get('from')
        to_currency = data.get('to')
        amount_money = float(data.get('amount'))

        if from_currency == to_currency:
            pass

        else:
            if from_currency == 'UER':
                # Convert to rubles
                first = user_data.amount_euro * float(data_rate.get('UER'))

            elif from_currency == 'USD':
                # Convert to rubles
                first = user_data.amount_dollars * float(data_rate.get('USD'))

            else:
                first = user_data.amount_rubles

            if first < amount_money * float(data_rate.get(from_currency, 1)):
                error = 'Cant convert money. You have not enough money.'

            else:
                second = first / float(data_rate.get(to_currency, 1))

                if to_currency == 'EUR':
                    user_data.update(amount_euro=user_data.get(
                        'amount_euro') + second)

                elif to_currency == 'USD':
                    user_data.update(amount_dollars=user_data.get(
                        'amount_dollars') + second)

                else:
                    user_data.update(amount_rubles=user_data.get(
                        'amount_rubles') + second)

                if from_currency == 'EUR':
                    user_data.update(amount_euro=user_data.get(
                        'amount_euro') - amount_money)

                elif to_currency == 'USD':
                    user_data.update(amount_dollars=user_data.get(
                        'amount_dollars') - amount_money)

                else:
                    user_data.update(amount_rubles=user_data.get(
                        'amount_rubles') - amount_money)

    name_user = str(request.user.username)
    return render(request, 'wallet/convert.html',
                  {'user_data': user_data,
                   'name': name_user,
                   'rate_eur': data_rate.get('EUR'),
                   'rate_usd': data_rate.get('USD'),
                   'error': error
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
    data_rate = return_todays_rate()
    user_data = Wallets.objects.get(user=request.user)
    name_user = str(request.user.username)

    return render(request, 'wallet/topup.html',
                  {'user_data': user_data,
                   'name': name_user,
                   'rate_eur': data_rate.get('EUR'),
                   'rate_usd': data_rate.get('USD'),
                   })


@login_required
def withdraw_money(request, user_id):
    '''
    Withdraw money from the system.
    '''
