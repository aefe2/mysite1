from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as authViews
from .views import RegisterView, LoginView, EditProfileView, UserPasswordChangeView, DeleteUserView

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('profile/', views.profile, name='profile'),
    path('logout/', authViews.LogoutView.as_view(next_page='polls:index'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile_edit/', EditProfileView.as_view(), name='edit'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('profile_delete/', DeleteUserView.as_view(), name='user_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
