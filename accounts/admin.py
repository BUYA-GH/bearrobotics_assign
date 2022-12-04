from django.contrib import admin

from .models import Card, Account, Transaction

# Register your models here.
class CardAdmin(admin.ModelAdmin):
    search_fields = ('cardNum', )
    list_display = ('cardNum', )

class AccountAdmin(admin.ModelAdmin):
    search_fields = ('accountNumber', 'author__cardNum', )
    list_display = ('accountNumber', 'author', 'balance', )

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('account__accountNumber', )
    list_display = ('account', 'receivedPaid', 'transact_at', )

admin.site.register(Card, CardAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)