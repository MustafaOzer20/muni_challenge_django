from django.urls import path
from .views import UserViewset


urlpatterns = [
    path('register', UserViewset.as_view({'post':'register'})),
    path('login', UserViewset.as_view({'post':'login'})),
    path('user', UserViewset.as_view({'get':'viewUser'})),
    path('logout', UserViewset.as_view({'post':'logout'})),
]