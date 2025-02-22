from django.urls import path
from .views import register_user
from .views import donate
from .views import login_view
from .views import ngo_stats
from .views import NotificationView
from .views import CreateFundPostView  # Ensure this import is correct




urlpatterns = [
    path('register/', register_user, name='register'),
    path('donate/', donate, name='donate'),
    path('login/', login_view, name='login'),
    path('api/ngo-stats/<int:ngo_id>/', ngo_stats, name="ngo-stats"),
    path("api/notifications/", NotificationView.as_view(), name="notifications"),
    path('api/create-fund-post/', CreateFundPostView.as_view(), name='create-fund-post'),

]
