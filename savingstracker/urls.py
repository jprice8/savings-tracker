from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from tracker import views as tracker_views

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # auth urls
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # landing urls
    path('', tracker_views.index, name='landing'),

    # tracker urls
    path('tracker/', include('tracker.urls')),
]
