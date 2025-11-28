from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # User Profile
    path('user/', views.UserDetailView.as_view(), name='user_detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('stats/', views.user_stats, name='user_stats'),
    
    # Skills Management
    path('skills/add/', views.AddSkillView.as_view(), name='add_skill'),
    path('skills/remove/', views.RemoveSkillView.as_view(), name='remove_skill'),
]
