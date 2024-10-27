from django.urls import path
from .views import Signup, Logout, Profile, Login



urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('signup/', Signup.as_view(), name="signup"),
    path('logout/', Logout.as_view(), name="logout"),
    path('profile/', Profile.as_view(), name="profile"),
]