from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, get_list_or_404
from .models import Client, AmountAdded, ClearedClients, BalanceSheet
from .forms import ClientForm, SearchBar, ReturneeForm, SavingsWithdraw, AmountAddedForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

#Index Page, Login required
@login_required(login_url='/login')
def index(request):
    Clients = Client.objects.all().filter(cleared=False)
    ClearedClis = ClearedClients.objects.filter(client__cleared=True).order_by('client__idField', '-date').distinct('client__idField')
    
    if request.method == "GET":
        form = SearchBar(request.GET)
        if form.is_valid():
            search = form.cleaned_data['searchVal']
            return redirect('Accounts:search', clientNo=search)   
    else:
        form = SearchBar()
    context = {
        'client': Clients,
        'cleared': ClearedClis,
        'form': form,
        'name': request.user.username,
    }
    return render(request, 'account/index.html', context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.GET)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect(request.GET.get('next'))
            else:
                messages.error(request, "Invalid Username or Password")
        else:
            print(form.errors)
            messages.error(request, "Something went wrong")
    
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)

#Search View Logic
@login_required(login_url='/login')
def search(request, clientNo):
    client = get_object_or_404(Client, idField=clientNo)
    cleared = False
    if client.amount == None:
        cleared = True
        client = get_list_or_404(ClearedClients.objects.order_by("-date"), client__idField=clientNo)
    if request.method == "GET":
        form = SearchBar(request.GET)
        if form.is_valid():
            search = form.cleaned_data['searchVal']
            return redirect('Accounts:search', clientNo=search)
    else:
        form = SearchBar()
    context = {
        'client':client,
        'form':form,
        'cleared': cleared,
        'name': request.user.username,
    }
    return render(request, 'account/search.html', context)

#Client Savings Withdrawal Logic
@login_required(login_url='/login')
def withdrawSavings(request, accountNum):
    clientWithdraw = Client.objects.get(idField=accountNum)
    if request.method == 'POST':
        form = SavingsWithdraw(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amountWithdrawn']
            newSave = clientWithdraw.savings - amount
            clientWithdraw.savings=newSave
            clientWithdraw.save()
        return redirect('/')
    else:
        form = SavingsWithdraw()
    context = {
        'form': form,
        'client': clientWithdraw,
        'name': request.user.username,
    }
    return render(request, 'account/saveWithdraw.html', context)

#Sorted Client View
@login_required(login_url='/login')
def sortIndex(request, sortParam, order):
    if order == 'asc':
        order = 'dsc'
    else:
        sortParam = '-' + sortParam
        order='asc'
    Clients = Client.objects.all().filter(cleared=False).order_by(sortParam)
    money = AmountAdded.objects.all()  
    ClearedClis = ClearedClients.objects.all()
    context = {
        'client': Clients,
        'money':money,
        'order':order,
        'cleared':ClearedClis,
        'name': request.user.username,
    }
    return render(request, 'account/sortIndex.html', context)

#Client Debt View
@login_required(login_url='/login')
def debtView(request, accountNum):
    client = Client.objects.get(idField = accountNum)
    money = AmountAdded.objects.filter(client__idField=accountNum)
    context = {
        'client': client,
        'money': money,
        'name': request.user.username,
    }
    return render(request, 'account/debtDetails.html', context)

#Clients CLeared Debt View
@login_required(login_url='/login')
def clearedDebtView(request, accountNum):
    client = Client.objects.get(idField = accountNum)
    money = ClearedClients.objects.filter(client__idField=accountNum)
    context = {
        'client': client,
        'money': money,
        'name': request.user.username,
    }
    return render(request, 'account/clearedDetails.html', context)


@login_required(login_url='/login')
def clearedDebtDetail(request, accountNum, debtId):
    client = Client.objects.get(idField = accountNum)
    money = ClearedClients.objects.get(client__idField=accountNum, pk = debtId)
    count = range(len(money.weeklyPays))
    count = [i+1 for i in count]
    context = {
        'client': client,
        'money': money,
        'count': count,
        'name': request.user.username,
    }
    return render(request, 'account/clearedDetailsExp.html', context)

#UpdateClient View
@login_required(login_url='/login')
def updateClientField(request, accountNum):
    client = Client.objects.get(idField = accountNum)
    if request.method == 'POST':
        form = AmountAddedForm(request.POST)
        if form.is_valid():
            amtPaid = form.cleaned_data['amountPaid']
            amtSaved = form.cleaned_data['amountSaved']
            AmountAdded.objects.create(client=client, amountPaid=amtPaid, amountSaved=amtSaved)
            return redirect('/')
    else:
        form = AmountAddedForm()
        context = {
            'form': form,
            'client': client,
            'name': request.user.username,
        }
        
        return render(request, 'account/updatePay.html', context)

#Create Loan View
@login_required(login_url='/login')
def loanCreate(request, clientStatus):
    if clientStatus == 'new':
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                phone = form.cleaned_data['phone']
                home = form.cleaned_data['homeAddress']
                shop = form.cleaned_data['shopAddress']
                work = form.cleaned_data['work']
                guarantorName = form.cleaned_data['guarantorName']
                guarantorAddress = form.cleaned_data['guarantorAddress']
                guarantorPhone = form.cleaned_data['guarantorPhone']
                amount = form.cleaned_data['amount']

                Client.objects.create(name=name, amount=amount, phone=phone,\
                homeAddress=home, shopAddress=shop, work=work, guarantorName=guarantorName, guarantorAddress=guarantorAddress, guarantorPhone=guarantorPhone)
                return redirect('/')
        else:
            form = ClientForm()
            context = {
                'form': form,
                'name': request.user.username,
            }
            return render(request, 'account/addClient.html', context)
    else:
        ClearedClis = ClearedClients.objects.filter(client__cleared=True).order_by('client__idField', '-date').distinct('client__idField')
        single=False
        if request.method == "GET":
            form = SearchBar(request.GET)
            if form.is_valid():
                search = form.cleaned_data['searchVal']
                ClearedClis = get_object_or_404(Client, idField=search, cleared=True)
                single = True
        else:
            form = SearchBar()
        context = {
            'cleared': ClearedClis,
            'form': form,
            'single': single,
            'name': request.user.username,
        }
        return render(request, 'account/clientReturn.html', context)

#Returnee PayView
@login_required(login_url='/login')
def returneePayView(request, accountNum):
    client = Client.objects.get(idField=accountNum)
    if request.method == 'POST':
        form = ReturneeForm(request.POST)
        if form.is_valid():
            amountGiven = form.cleaned_data['amount']
            client.amount = amountGiven
            client.restart = True
            client.cleared = False
            client.color = 'rgb(58, 58, 172)'
            client.save()
            return redirect('/')
    else:
        form = ReturneeForm()
    context = {
        'client': client,
        'form': form,
        'name': request.user.username,
    }
    return render(request, 'account/addReturn.html', context)

#Book keeping Balance Sheet
@login_required(login_url='/login')
def balancesheet(request):
    cash = BalanceSheet.objects.last()
    color='green'
    if cash.percentgrowth < 0:
        color = 'red'
    context = {
        'name': request.user.username,
        'bsheet': cash,
        'color': color,
    }
    return render(request, 'account/efeinfo.html', context)

#Logout 
def logout_view(request):
    logout(request)
    return redirect('Accounts:login')