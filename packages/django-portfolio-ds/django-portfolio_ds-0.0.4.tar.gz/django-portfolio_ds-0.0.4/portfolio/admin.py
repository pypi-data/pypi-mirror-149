from django.contrib import admin
from .models import Portfolio, Category

import django.contrib.auth.models
from django.contrib import auth


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'filter')
    search_fields = ['title']


admin.site.register(Category)
admin.site.register(Portfolio, PortfolioAdmin)
try:
    admin.site.unregister(auth.models.User)
    admin.site.unregister(auth.models.Group)
except django.contrib.admin.sites.NotRegistered:
    pass

