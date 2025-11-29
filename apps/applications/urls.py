from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # List and Create
    path('', views.ApplicationListCreateView.as_view(),
         name='application_list_create'),

    # Statistics and Search (must come before <str:pk>)
    path('stats/', views.application_statistics, name='application_statistics'),
    path('search/', views.search_applications, name='search_applications'),

    # Detail, Update, Delete
    path('<str:pk>/', views.ApplicationDetailView.as_view(),
         name='application_detail'),

    # Timeline
    path('<str:pk>/timeline/', views.add_timeline_event, name='add_timeline_event'),

    # Status Update
    path('<str:pk>/status/', views.update_status, name='update_status'),
]
