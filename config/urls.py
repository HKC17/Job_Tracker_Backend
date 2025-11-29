from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Job Application Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
                'refresh': '/api/auth/refresh/',
                'logout': '/api/auth/logout/',
                'user': '/api/auth/user/',
                'change_password': '/api/auth/change-password/',
                'stats': '/api/auth/stats/',
            },
            'applications': {
                'list': '/api/applications/',
                'create': '/api/applications/',
                'detail': '/api/applications/{id}/',
                'timeline': '/api/applications/{id}/timeline/',
                'status': '/api/applications/{id}/status/',
                'stats': '/api/applications/stats/',
                'search': '/api/applications/search/?q=term',
            },
            'analytics': {
                'dashboard': '/api/analytics/dashboard/',
                'applications_over_time': '/api/analytics/applications-over-time/?period=month',
                'success_rate': '/api/analytics/success-rate/',
                'skills': '/api/analytics/skills/',
                'timeline': '/api/analytics/timeline/',
                'salary': '/api/analytics/salary/',
                'response_time': '/api/analytics/response-time/',
            }
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api_root'),
    path('api/auth/', include('apps.users.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
