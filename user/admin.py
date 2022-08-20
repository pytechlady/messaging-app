from django.contrib import admin
from .models import Message, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_filter = ('username',)
    search_fields = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(Message)