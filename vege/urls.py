from django.urls import path
from .import views

urlpatterns = [
    path('',views.login_page,name="login_page"),
    path('logout/',views.logout_page,name="logout_page"),
    path('registration/',views.register_page,name="register_page"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('update/<int:id>/',views.update_recipe,name="update_recipe"),
    path('delete/<int:id>/',views.delete_recipe,name="delete_recipe"),
]
