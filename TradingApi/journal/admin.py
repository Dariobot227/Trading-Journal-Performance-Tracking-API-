from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Trade, Strategy, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "is_staff", "is_superuser")
    search_fields = ("username", "email")

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("user",)
    search_fields = ("name", "user__username")
    ordering = ("user",)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("id","user","pair","direction","lot_size","status","profit_loss","opened_at",)
    list_filter = ("user","pair","direction","status","emotion",)
    search_fields = ("user__username","pair",)
    ordering = ("-opened_at",)
    list_per_page = 25


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "Account_size", "current_balance")
    search_fields = ("user__username",)
    ordering = ("user",)