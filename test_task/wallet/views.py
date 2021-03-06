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
    data_rate = return_todays_rate()
    name_user = str(request.user.username)
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
    user_data = Wallets.objects.get(user=request.user)
    data_rate = return_todays_rate()
    name_user = str(request.user.username)
    error = ''

    if request.method == 'POST':
        data = request.POST
        from_currency = data.get('from')
        to_currency = data.get('to')
        amount_money = float(data.get('amount'))

        if from_currency == to_currency:
            pass

        else:
            substract_from = amount_money
            add_to = amount_money * \
                float(data_rate.get(from_currency, 1)) / \
                float(data_rate.get(to_currency, 1))

            if from_currency == 'UER' and user_data.amount_euro < substract_from or \
                    from_currency == 'USD' and user_data.amount_dollars < substract_from or \
                    from_currency == 'RUB' and user_data.amount_rubles < substract_from:

                error = 'Cant convert money. You have not enough money.'

            else:
                if from_currency == 'EUR':
                    user_data.amount_euro = user_data.amount_euro - substract_from
                    user_data.save()

                elif from_currency == 'USD':
                    user_data.amount_dollars = user_data.amount_dollars - substract_from
                    user_data.save()

                else:
                    user_data.amount_rubles = user_data.amount_rubles - substract_from
                    user_data.save()

                if to_currency == 'EUR':
                    user_data.amount_euro = user_data.amount_euro + add_to
                    user_data.save()

                elif to_currency == 'USD':
                    user_data.amount_dollars = user_data.amount_dollars + add_to
                    user_data.save()

                else:
                    user_data.amount_rubles = user_data.amount_rubles + add_to
                    user_data.save()

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
    user_data = Wallets.objects.get(user=request.user)
    data_rate = return_todays_rate()
    name_user = str(request.user.username)
    error = ''
    if request.method == 'POST':
        data = request.POST
        print(data)
        target_username = data.get('user')
        currency = data.get('currency')
        amount = float(data.get('amount'))

        target_user = User.objects.get(username=target_username)
        target_wallet = Wallets.objects.get(user=target_user)

        if currency == 'EUR' and user_data.amount_euro > amount:
            target_wallet.amount_euro = target_wallet.amount_euro + amount
            target_wallet.save()

            user_data.amount_euro = user_data.amount_euro - amount
            user_data.save()

        elif currency == 'USD' and user_data.amount_dollars > amount:
            target_wallet.amount_dollars = target_wallet.amount_dollars + amount
            target_wallet.save()

            user_data.amount_dollars = user_data.amount_dollars - amount
            user_data.save()
        elif currency == 'RUB' and user_data.amount_rubles > amount:
            target_wallet.amount_rubles = target_wallet.amount_rubles + amount
            target_wallet.save()

            user_data.amount_rubles = user_data.amount_rubles - amount
            user_data.save()
        else:
            error = 'You have not enough money for transferring.'

    all_users = User.objects.all().exclude(
        username='admin').exclude(username=name_user)

    return render(request, 'wallet/transfer.html',
                  {'user_data': user_data,
                   'name': name_user,
                   'rate_eur': data_rate.get('EUR'),
                   'rate_usd': data_rate.get('USD'),
                   'all_users': all_users,
                   'error': error
                   })


@login_required
def top_up_account(request):
    '''
    Top up an account.
    '''
    user_data = Wallets.objects.get(user=request.user)
    data_rate = return_todays_rate()
    name_user = str(request.user.username)
    if request.method == 'POST':
        data = request.POST
        currency = data.get('currency')
        amount_money = float(data.get('amount'))

        if currency == 'EUR':
            user_data.amount_euro = user_data.amount_euro + amount_money
            user_data.save()

        elif currency == 'USD':
            user_data.amount_dollars = user_data.amount_dollars + amount_money
            user_data.save()

        else:
            user_data.amount_rubles = user_data.amount_rubles + amount_money
            user_data.save()

    return render(request, 'wallet/topup.html',
                  {'user_data': user_data,
                   'name': name_user,
                   'rate_eur': data_rate.get('EUR'),
                   'rate_usd': data_rate.get('USD'),
                   })


@login_required
def withdraw_money(request):
    '''
    Withdraw money from the system.
    '''
    user_data = Wallets.objects.get(user=request.user)
    data_rate = return_todays_rate()
    name_user = str(request.user.username)
    error = ''

    if request.method == 'POST':
        data = request.POST
        currency = data.get('currency')
        amount_money = float(data.get('amount'))

        if currency == 'EUR':
            if user_data.amount_euro - amount_money >= 0:
                user_data.amount_euro = user_data.amount_euro - amount_money
                user_data.save()

            else:
                error = 'Cant withdraw money. You have not enough money.'

        elif currency == 'USD':
            if user_data.amount_dollars - amount_money >= 0:
                user_data.amount_dollars = user_data.amount_dollars - amount_money
                user_data.save()

            else:
                error = 'Cant withdraw money. You have not enough money.'

        else:
            if user_data.amount_rubles - amount_money >= 0:
                user_data.amount_rubles = user_data.amount_rubles - amount_money
                user_data.save()
            else:
                error = 'Cant withdraw money. You have not enough money.'

    return render(request, 'wallet/withdraw.html',
                  {'user_data': user_data,
                   'name': name_user,
                   'rate_eur': data_rate.get('EUR'),
                   'rate_usd': data_rate.get('USD'),
                   'error': error
                   })
