from django.contrib import admin
from django.urls import path, include
from .views import CustomObtainAuthToken


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', CustomObtainAuthToken.as_view()),
    path('api/',  include('csv_gen.urls'))
]
