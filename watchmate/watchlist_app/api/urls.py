from django.urls import path, include
from watchlist_app.api.views import ReviewList, ReviewDetails, ReviewCreate, StreamPlatformV, WatchListV
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('platform', StreamPlatformV, basename='streamplatform')
router.register('list', WatchListV, basename='watchlist')




urlpatterns = [
    # path('list/', WatchListAV.as_view(), name='watchlist'),
    # path('list/<int:id>', WatchDetailsAV.as_view(), name='watchlist-detail'),
    # path('platform/', StreamPlatformAV.as_view(), name='streamplatform-list'),
    # path('platform/<int:id>', StreamPlatformDetailsAV.as_view(), name='streamplatform-detail'),
    path('', include(router.urls)),
    path('movie/<int:pk>/reviews/', ReviewList.as_view(), name='reviews'),
    path('movie/<int:pk>/review-create/', ReviewCreate.as_view(), name='reviews'),
    path('movie/review/<int:pk>/', ReviewDetails.as_view(), name='reviews-details'),

] 

