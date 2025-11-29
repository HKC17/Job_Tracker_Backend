from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    # List and Create
    path('', views.CompanyListCreateView.as_view(), name='company_list_create'),

    # Search and Autocomplete (must come before <str:pk>)
    path('search/', views.search_companies, name='search_companies'),
    path('autocomplete/', views.autocomplete_companies,
         name='autocomplete_companies'),
    path('sync/', views.sync_companies, name='sync_companies'),
    path('industry-breakdown/', views.industry_breakdown,
         name='industry_breakdown'),
    path('top/', views.top_companies, name='top_companies'),

    # Detail, Update, Delete
    path('<str:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),

    # Company-specific endpoints
    path('<str:pk>/applications/', views.company_applications,
         name='company_applications'),
    path('<str:pk>/stats/', views.company_stats, name='company_stats'),
]
