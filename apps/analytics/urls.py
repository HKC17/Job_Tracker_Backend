from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),

    # Time Series
    path('applications-over-time/', views.applications_over_time,
         name='applications_over_time'),
    path('success-rate/', views.success_rate_over_time, name='success_rate'),

    # Insights
    path('skills/', views.skills_demand, name='skills_demand'),
    path('timeline/', views.timeline_analysis, name='timeline_analysis'),
    path('salary/', views.salary_insights, name='salary_insights'),
    path('response-time/', views.response_time_analysis, name='response_time'),
]
