from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class BalanceSheet(models.Model):
    year = models.IntegerField()
    bankbalance = models.IntegerField()
    cashbalance = models.IntegerField()
    totaldebt = models.IntegerField()
    totalowed = models.IntegerField()
    capitalinvested = models.IntegerField()
    companyworth = models.IntegerField(blank=True)
    percentgrowth = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.year)

    def save(self, *args, **kwargs):
        self.totalowed = max(sum(Client.objects.filter(cleared=False).values_list('deficit', flat=True)), self.totalowed)
        self.companyworth = self.bankbalance + self.cashbalance + self.totalowed - self.totaldebt
        self.percentgrowth = ((self.companyworth - self.capitalinvested) / self.capitalinvested) * 100
        super(BalanceSheet, self).save(*args, **kwargs)

class Client(models.Model):
    name = models.CharField(max_length=50)
    idField = models.IntegerField()
    phone = models.CharField(max_length=13)
    homeAddress = models.CharField(max_length=100)
    shopAddress = models.CharField(max_length=100)
    work = models.CharField(max_length=50)
    guarantorName = models.CharField(max_length=50)
    guarantorAddress = models.CharField(max_length=50)
    guarantorPhone = models.CharField(max_length=13)
    amount = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    savings = models.IntegerField(null=True, blank=True)
    deficit = models.IntegerField(null=True, blank=True)
    cleared = models.BooleanField(default=False)
    restart = models.BooleanField(default=True)
    color = models.CharField(max_length=1000, default="rgb(235, 235, 235)")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.idField == None:
            self.idField = 10000 + Client.objects.count()
        if self.savings == None:
            self.savings = 0
        if self.restart:
            self.date = datetime.date(datetime.now())
        if self.deficit == None:
            self.deficit = self.amount
        elif self.deficit > 0:
            self.cleared = False
        super(Client, self).save(*args, **kwargs)

class AmountAdded(models.Model):
    client = models.ForeignKey(Client, related_name='person', on_delete=models.CASCADE)
    amountPaid = models.IntegerField()
    amountSaved = models.IntegerField()
    date_paid = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        addeds = AmountAdded.objects.all().filter(client__idField=self.client.idField)
        self.client.deficit = self.client.amount - sum(addeds.values_list('amountPaid', flat=True)) - self.amountPaid
        self.client.savings = self.amountSaved + self.client.savings
        addedsList = list(addeds.values_list('amountPaid', flat=True))
        print(addedsList)
        if addedsList.count(0) > 2:
            self.client.color = 'rgb(205, 15, 15)'

        if self.client.deficit <= 0:
            wkpay = list(addeds.values_list('amountPaid', flat=True))
            wkpay.append(self.amountPaid)
            self.client.cleared = True
            createClearedClient(self.client, wkpay)
            self.client.amount = None
            AmountAdded.objects.filter(client__idField=self.client.idField).delete()
            self.client.deficit = None
            self.client.restart = True
            self.client.color = 'green'
            self.client.save()
        else:
            self.client.cleared = False
            self.client.restart = False
            self.client.save()
            super(AmountAdded, self).save(*args, **kwargs)
        
        
class ClearedClients(models.Model):
    client = models.ForeignKey(Client, related_name='client', on_delete=models.CASCADE)
    amounts = models.IntegerField()
    date = models.DateField()
    weeklyPays = ArrayField(
        models.IntegerField()
    )
    clearedDate = models.DateField(auto_now_add=True)

def createClearedClient(client, payList):
    ClearedClients.objects.create(client=client, amounts=client.amount, date=client.date, weeklyPays=payList)

    