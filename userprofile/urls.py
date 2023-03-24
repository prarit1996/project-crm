from django.urls import path
from .views import signup,myaccount
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
app_name='userprofile'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name = 'userprofile/login.html', authentication_form = LoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('myaccount/', myaccount, name='myaccount')
]