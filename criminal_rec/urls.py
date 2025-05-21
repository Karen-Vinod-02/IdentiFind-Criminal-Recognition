from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views.login_views import login_view, logout_view
from .views.surveillance_views import image_surveillance, capture_image, check_result, match_found  

urlpatterns = [
    path('', login_view, name='index'),
    path('image-surveillance/', image_surveillance, name='image-surveillance'),
    path('capture/', capture_image, name='capture-image'),
    path('check_result/', check_result, name='check-result'), 
    path('match_found/', match_found, name='match-found'),
    path('logout/', logout_view, name='logout'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
