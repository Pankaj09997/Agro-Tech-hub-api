from django.urls import path
from api.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView,PostView,CommentView,PostAllView,VideoView,VideoAll,UserListView,ChatHistoryView,ExpenseListCreateAPIView,ExpenseDetailAPIView,SelectRoleView,FarmerProductListView,FarmerProductDetailView,FarmerProductAddView,BuyerDetailView,BuyerListView,GetCartItemView,PostCartItemView,NotificationGet,NotificationPost
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import SubmitCitizenshipVerification


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
    path('videosall/',VideoAll.as_view(),name='videos'),
    path('usersall/',UserListView.as_view(),name="Userall"),
    path('api/chat-history/', ChatHistoryView.as_view(), name='chat-history'),
    path('expenses/', ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailAPIView.as_view(), name='expense-detail'),
    path('citizenship/submit/', SubmitCitizenshipVerification.as_view(), name='submit_citizenship_verification'),
     path('select-role/', SelectRoleView.as_view(), name='select_role'),
     path('farmerlist/', FarmerProductListView.as_view(), name='productlist'),
     path('farmerproductadd/', FarmerProductAddView.as_view(), name='addproduct'),
     path('detail/<int:id>/', FarmerProductDetailView.as_view(), name='detail'),
     path('buyerlist/', BuyerListView.as_view(), name='buyerlist'),
     path('buyerdetail/<int:id>/', BuyerDetailView.as_view(), name='productdetail'),
     path('addtocart/',PostCartItemView.as_view(),name='addtocart'),
     path('getcart/',GetCartItemView.as_view(),name='getcartitem'),
     path('chat-history/<int:me_id>/<int:frnd_id>/', ChatHistoryView.as_view(), name='chat-history'),
     path('notifications/', NotificationGet.as_view(), name='notification_get'),
     path('notifications/send/<int:id>/', NotificationPost.as_view(), name='notification_post'),
     



     
     

    

    
    
]
