from django.urls import path
from . import views


app_name = "users"


urlpatterns = [
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("login/", views.login_view, name="login"),
    path("account/", views.AccountPageView.as_view(), name="account"),
    path("account_update/<int:pk>/", views.AccountUpdateView.as_view(), name="account_update"),
    path("logout/", views.logout_view, name="logout")
]
