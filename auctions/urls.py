from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:p_id>", views.listing, name="listing"),
    path("comments/<int:p_id>", views.add_comment, name="add_comment"),
    path("addbid/<int:p_id>", views.add_bid, name="add_bid"),
    path("search/", views.search_items, name="search_items"),
    path("category/", views.category, name="category"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watch/<int:id>", login_required(views.watch), name="watch"),
    path("unwatch/<int:id>", views.unwatch, name="unwatch"),
    path("create/", views.create, name="create"),
    path("insert/", views.insert, name="insert"),
    path("closebid/<int:p_id>", views.close_bid, name="close_bid"),
    path("delbid/<int:p_id>", views.del_bid, name="del_bid"),
]
