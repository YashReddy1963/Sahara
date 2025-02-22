from django.urls import path
from .views import register_user
from .views import donate
from .views import login_view
from .views import create_fund_post
from .views import ngo_stats
from .views import NotificationView
from .views import FundPostDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ngo_registration
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('api/ngo/register/', ngo_registration, name='ngo_registration'),
    path('donate/', donate, name='donate'),
    path('fund-posts/create/', create_fund_post, name='create_fund_post'),
    path('api/ngo-stats/<int:ngo_id>/', ngo_stats, name="ngo-stats"),
    path("api/notifications/", NotificationView.as_view(), name="notifications"),
    path("api/fund-posts/<int:post_id>/", FundPostDetailView.as_view(), name="fund_post_detail"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (Get Access & Refresh Token)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)