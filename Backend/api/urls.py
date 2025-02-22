from django.urls import path
from .views import register_user
from .views import donate
from .views import login_view
from .views import ngo_stats
from .views import NotificationView
from .views import FundPostDetailView
from .views import CreateFundPostView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ngo_registration
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'),
    path('api/ngo/register/', ngo_registration, name='ngo_registration'),
    path('api/create-fund-post/', CreateFundPostView.as_view(), name='create-fund-post'),
    path("api/fund-posts/", FundPostDetailView.as_view(), name="all_fund_posts"),  # Fetch all posts
    path("api/fund-posts/<int:post_id>/", FundPostDetailView.as_view(), name="single_fund_post"),  # Fetch one post
    path('donate/', donate, name='donate'),
    path('api/ngo-stats/<int:ngo_id>/', ngo_stats, name="ngo-stats"),
    path("api/notifications/", NotificationView.as_view(), name="notifications"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)