from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, get_list_or_404
from .models import Client, AmountAdded, ClearedClients, BalanceSheet
from .forms import ClientForm, SearchBar, ReturneeForm, SavingsWithdraw, AmountAddedForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid Username or Password")
        else:
            messages.error(request, "Something went wrong")
    
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)
    

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
        'cleared': cleared
    }
    return render(request, 'account/search.html', context)

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
    }
    return render(request, 'account/saveWithdraw.html', context)

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
    }
    return render(request, 'account/sortIndex.html', context)

def debtView(request, accountNum):
    client = Client.objects.get(idField = accountNum)
    money = AmountAdded.objects.filter(client__idField=accountNum)
    context = {
        'client': client,
        'money': money,
    }
    return render(request, 'account/debtDetails.html', context)


def clearedDebtView(request, accountNum):
    client = Client.objects.get(idField = accountNum)
    money = ClearedClients.objects.filter(client__idField=accountNum)
    context = {
        'client': client,
        'money': money,
    }
    return render(request, 'account/clearedDetails.html', context)

def clearedDebtDetail(request, accountNum, debtId):
    client = Client.objects.get(idField = accountNum)
    money = ClearedClients.objects.get(client__idField=accountNum, pk = debtId)
    count = range(len(money.weeklyPays))
    count = [i+1 for i in count]
    context = {
        'client': client,
        'money': money,
        'count': count,
    }
    return render(request, 'account/clearedDetailsExp.html', context)

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
        }
        
        return render(request, 'account/updatePay.html', context)

def giveLoan(request):
    return render(request, 'account/loanOpt.html')

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
        }
        return render(request, 'account/clientReturn.html', context)

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
    }
    return render(request, 'account/addReturn.html', context)

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

def logout_view(request):
    logout(request)
    return redirect('Accounts:login')