from django.urls import path
from . import views


urlpatterns = [
    path('wallet/', views.user_wallets, name='user_wallets'),
    path('convert/', views.convert_money, name='convert_money'),
    path('transfer/', views.transfer_money, name='transfer_money'),
    path('topup/', views.top_up_account, name='top_up_account'),
    path('withdraw/', views.withdraw_money, name='withdraw_money'),
]
