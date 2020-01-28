from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register),  # POST
    path('quotes', views.quotes),  # GET
    path('logout', views.logout),  # GET
    path('login', views.login),  # POST
    path('new_quote', views.new_quote),
    path('profile/<int:id>', views.profile),
    path('profile/<int:id>/edit', views.edit_profile),
    path('profile/<int:id>/update', views.update_profile),
    path('quote/<int:id>/delete', views.delete_quote),
]
