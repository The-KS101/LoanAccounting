from django.urls import path
from . import views

app_name='Accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('clients/<int:accountNum>/payDetails', views.debtView, name="debtPayments"),
    path('index/sortBy=<str:sortParam>?ord=<str:order>', views.sortIndex, name="sortInd"),
    path('clients/<int:accountNum>/clearedDebt/', views.clearedDebtView, name="clearView"),
    path('clients/<int:accountNum>/clearedDebt/expandView-<int:debtId>', views.clearedDebtDetail, name="clearViewDet"),
    path('clients/<int:accountNum>/paymentsMade', views.updateClientField, name="makePay"),
    path('clients/<str:clientStatus>/createNew', views.loanCreate, name="createLoan"),
    path('clients/loanReturnee/<int:accountNum>', views.returneePayView, name="returneeLoan"),
    path('clients/SavingsWithdrawal/<int:accountNum>', views.withdrawSavings, name="withdraw"),
    path('search/<int:clientNo>', views.search, name="search"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('accounts/balance-sheet-info', views.balancesheet, name='balance')
]