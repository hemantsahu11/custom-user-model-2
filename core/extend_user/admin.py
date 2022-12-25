from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from .models import NewUser

# Register your models here.

# admin.site.register(NewUser, UserAdmin)    # by default extended user class will not be displayed on the screen so we have to register this by using NewUser, UserAdmin
# but this UserAdmin will not show extra field to the website
# 1st approach

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Additional Info',
#             {
#                 'fields': (
#                     'age',
#                     'nickname'
#                 )
#             }
#         )
#     )
#
#
# admin.site.register(NewUser, CustomUserAdmin)   # now by using this class CustomUserAdmin this will be displayed on the screen

# 2nd approach

# fields = list(UserAdmin.fieldsets)
# fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'age', 'nickname', 'user_type')})
# UserAdmin.fieldsets = tuple(fields)    # by using this option additional fields will be shown to Personal Info section
# admin.site.register(NewUser, UserAdmin)


""" to reorder things """


class UserAdminConfig(UserAdmin):    # whenever we want to make some changes to predefined user table and ordering we have to override UserAdmin class
    search_fields = ('email', 'user_name', 'first_name', )
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)   # users will display in the reverse order of date
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')

    fieldsets = (    # reordering that panels or field sets
        (None, {'fields': ('email', 'user_name', 'first_name')}),
        ('Permissions', {'fields':('is_staff', 'is_active')}),
        ('Personal', {'fields':('about', )}),
    )
    formfield_overrides = {
        NewUser.about : {'widget': Textarea(attrs={'rows':10, 'cols':40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password', 'password2', 'is_active', 'is_staff')
        }),
    )


admin.site.register(NewUser, UserAdminConfig)


