from django.contrib import admin

from .models import Lot, AdminProfile, AuctionHistory, UserProfile, Ban

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'name_lot',
                    'link_seller',
                    'address',
                    'description',
                    'date_of_create',
                    'start_price',
                    'current_price',
                    'end_date_auction',
                    'creator',
                    'images'
                    ]

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['lot',
                    'balance',
                    'status_buying',
                    'active_lot',
                    'rules',
                    'step_bid',
                    'current_price',
                    'user_name_bid',
                    'scheduled_time']

@admin.register(AuctionHistory)
class AuctionHistoryAdmin(admin.ModelAdmin):
    list_display = ['buyer',
                    'lot',
                    'current_price']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'access',
                    'balance',
                    'pay_counts']

@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'count_ban']
