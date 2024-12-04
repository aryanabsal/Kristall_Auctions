from django.contrib import admin
from .models import User, AuctionListing, Comment, Bid

# Register your models here.
admin.site.register(User)



class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'price', 'start_bid', 'created_at']

admin.site.register(AuctionListing, AuctionListingAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'auction', 'created_at']

admin.site.register(Bid, BidAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'auction', 'created_at']

admin.site.register(Comment, CommentAdmin)
