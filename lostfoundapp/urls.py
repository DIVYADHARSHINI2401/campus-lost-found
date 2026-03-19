from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/', views.post_item, name='post_item'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]