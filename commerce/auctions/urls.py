from django.urls import path

from . import views
app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("<int:id>/visit", views.visit,name="visit"),
    path("categories", views.categories, name="categories"),
    path("<str:category>/category_list",views.category_list, name="category_list"),
    path("watchlist",views.Watchlist,name="watchlist"),
    path("<int:id>/biding",views.biding,name="biding"),
     path("<int:id>/deactivate",views.deactivate,name="deactivate"),
     path("<int:id>/comment",views.comment,name="comment"),
     path("<int:id>/adding_to_watchlist",views.adding_to_watchlist,name="addtowatchlist"),
]
