from django.contrib import admin
from .models import AmountAdded, Client, BalanceSheet
# Register your models here.

class AmountAddedInline(admin.StackedInline):
    model=AmountAdded

class ClientAdmin(admin.ModelAdmin):
    inlines = [AmountAddedInline, ]

admin.site.register(Client, ClientAdmin)
admin.site.register(BalanceSheet)