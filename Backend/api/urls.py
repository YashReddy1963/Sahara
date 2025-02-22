from django.urls import path
from .views import register_user
from .views import donate
from .views import login_view
from .views import ngo_stats
from .views import NotificationView
from .views import CreateFundPostView  # Ensure this import is correct


from .views import FundPostDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ngo_registration
from django.conf.urls.static import static
from django.conf import settings

from .views import add_donation


urlpatterns = [
    path('register/', register_user, name='register'),
    path('donate/', donate, name='donate'),
    path('login/', login_view, name='login'),
    path('api/ngo-stats/<int:ngo_id>/', ngo_stats, name="ngo-stats"),
    path("api/notifications/", NotificationView.as_view(), name="notifications"),
    path('api/create-fund-post/', CreateFundPostView.as_view(), name='create-fund-post'),

    path("api/fund-posts/<int:post_id>/", FundPostDetailView.as_view(), name="fund_post_detail"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (Get Access & Refresh Token)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh Token
    path('api/ngo_register/', ngo_registration, name='ngo_registration'),
    path('api/add-donation/', add_donation, name='add_donation'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)