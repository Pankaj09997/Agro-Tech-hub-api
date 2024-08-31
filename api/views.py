from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import ChangePasswordSerializer, UserRegistrationSerializers, UserLoginSerializers, UserProfileSerializers, ChangePasswordSerializer,PostSerializers,CommentSerializers,VideoSerializers,VideoCommentSerializers,UserSerializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from api.models import Post,Comment,VideoComment,Video
from django.contrib.auth.models import User
from rest_framework import generics
from django.shortcuts import get_object_or_404
from api . models import MyUser
def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class UserRegistrationView(APIView):
    
    def post(self, request):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_token_for_user(user)
            return Response({"Token": token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializers = UserLoginSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            email = serializers.validated_data.get('email')
            password = serializers.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_token_for_user(user)
                return Response({"Token": token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializers = UserProfileSerializers(request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Successfully changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def post(self, request):
        serializers = PostSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save(author=request.user)
            return Response({'msg': 'You have successfully posted'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(commented_on=post).order_by('created_at')
        serializers = CommentSerializers(comments, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializers = CommentSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save(author=request.user, commented_on=post)
            return Response({'msg': 'You have successfully posted a comment'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostAllView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Post.objects.all().order_by('-created_at')
        serializers = PostSerializers(queryset, many=True)  # Correct context as dictionary
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class VideoView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializers=VideoSerializers(data=request.data)
        if (serializers.is_valid(raise_exception=True)):
            return Response({'msg':'You have successfully added a video',},status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Unable to add a video'},status=status.HTTP_400_BAD_REQUEST)
        
class VideoCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, video_id):
        video_content = get_object_or_404(Video, id=video_id)
        serializers = VideoCommentSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save(author=request.user, commented_on=video_content)
            return Response({'msg': 'You have successfully added a comment on a video'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, video_id):
        video_content = get_object_or_404(Video, id=video_id)
        comments = VideoComment.objects.filter(commented_on=video_content).order_by('-created_at')
        serializers = VideoCommentSerializers(comments, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
        
class VideoAll(APIView):
  permission_classes=[IsAuthenticated]
  def get(self,request):
    queryset=Video.objects.all().order_by('-uploaded_at')
    serializers=VideoSerializers(queryset,many=True)
    return Response(serializers.data,status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        # Query all users from MyUser instead of User
        queryset = MyUser.objects.all()
        serializers = UserSerializers(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
        
        
        
    

         
        
        
         
         
        
        
        
            

        

