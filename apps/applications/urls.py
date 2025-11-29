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

    # File uploads
    path('upload/', views.FileUploadView.as_view(), name='file_upload'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),

    # Detail, Update, Delete
    path('<str:pk>/', views.ApplicationDetailView.as_view(),
         name='application_detail'),

    # Timeline
    path('<str:pk>/timeline/', views.add_timeline_event, name='add_timeline_event'),

    # Status Update
    path('<str:pk>/status/', views.update_status, name='update_status'),

    # File attachments
    path('<str:pk>/attach/', views.attach_file_to_application, name='attach_file'),
    path('<str:pk>/attachments/<int:attachment_index>/',
         views.delete_attachment, name='delete_attachment'),
]
