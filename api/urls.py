from django.urls import path
from api.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView,PostView,CommentView,PostAllView,VideoView,VideoAll
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('post/',PostView.as_view(),name='postcontent'),
    path('postall/',PostAllView.as_view(),name='postall'),
    path('posts/<int:post_id>/comments/',CommentView.as_view(),name='comments'),
    path('videosUpload/',VideoView.as_view(),name='videosUpload'),
    path('videos/,<int:video_id>/comments/',VideoView.as_view(),name='videosComment'),
    path('videosall/',VideoAll.as_view(),name='videos')

    
    
]
