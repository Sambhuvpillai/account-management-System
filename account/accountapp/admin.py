from django.contrib import admin

# Register your models here.
from accountapp.models import *

# register model

admin.site.register(Employee)
admin.site.register(Leave)
