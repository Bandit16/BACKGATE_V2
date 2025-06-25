
from django.contrib import admin
from .models import *
admin.site.register(DefaultLiability)
admin.site.register(Transaction)
admin.site.register(MemberGroup)
admin.site.register(LedgerEntry)

class DefaultLiabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'user', 'group', 'due_date')
    list_filter = ('group',)
    search_fields = ('name', 'user__user__username', 'group__name')