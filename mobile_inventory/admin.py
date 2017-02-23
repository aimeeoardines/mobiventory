from django.contrib import admin

# Register your models here.
from .models import (
    Category,
    Device,
    Location,
    Staff,
    Status,
    Team,
    Transaction,
    TransactionBorrow,
    TransactionType,
    User,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', )
    search_field = ['category']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('category', 'status', 'model', 'serial_no', 'service_tag')
    search_field = ['category__category', 'status__is_available', 'model', 'serial_no', 'service_tag']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location', )
    search_field = ['location']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name')
    search_field = ['emp_id', 'name']


@admin.register(Status)
class Status(admin.ModelAdmin):
    list_display = ('health', 'image', 'is_available', 'notes', 'barcode', 'location')
    search_field = ['health', 'image', 'is_available', 'notes', 'barcode', 'location__location']


@admin.register(Team)
class Team(admin.ModelAdmin):
    list_display = ('name', )
    search_field = ['name']


@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ('staff', 'transaction_type', 'device', 'transaction_date')
    search_field = ['staff__name', 'transaction_type__transaction_type', 'device__name', 'transaction_date']


@admin.register(TransactionBorrow)
class TransactionBorrow(admin.ModelAdmin):
    list_display = ('expected_return_date', 'to_which_project')
    search_field = ['expected_return_date', 'to_which_project']


@admin.register(TransactionType)
class TransactionType(admin.ModelAdmin):
    list_display = ('transaction_type', )
    search_field = ['transaction_type']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name')
    search_field = ['emp_id', 'name']
