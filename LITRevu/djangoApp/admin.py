from django.contrib import admin
from .models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    search_fields = ('title', 'user__username')
    list_filter = ('time_created',)
    readonly_fields = ('time_created',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'rating', 'user', 'time_created')
    search_fields = ('headline', 'user__username')
    list_filter = ('time_created', 'rating')
    readonly_fields = ('time_created',)


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user', 'time_created')
    search_fields = ('user__username', 'followed_user__username')
    list_filter = ('time_created',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
