from django.contrib import admin

from . import models


class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('__str__', 'created', 'account', 'amount', 'verified', 'verified_at', 'modified')
    list_editable = ('amount', 'verified')
    list_filter = ('created', 'verified', 'verified_at')
    readonly_fields = ('token',)
    search_fields = ('account_username',)


class GatewayAdmin(admin.ModelAdmin):
    list_display = ('label', 'api_key', 'default_callback')
    list_editable = ('api_key',)
    search_fields = ('label',)


admin.site.register(models.Transaction, TransactionAdmin)
admin.site.register(models.Gateway, GatewayAdmin)
