from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import MyUserManager, MyUser,Post,Comment,Video,VideoComment,ChatModel



class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return MyUser.objects.create_user(**validated_data)

class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = MyUser
        fields = ["email", "password"]

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=32, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password)
        user.save()
        return attrs
    
class PostSerializers(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ['id','content', 'image', 'pdf', 'author_name', 'created_at']


        
class CommentSerializers(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name', read_only=True)
    commented_on = serializers.CharField(source='commented_on.content', read_only=True)

    class Meta:
        model = Comment
        fields = ['comment', 'author', 'commented_on', 'created_at']
        
class VideoSerializers(serializers.ModelSerializer):
    author=serializers.CharField(source='author.name',read_only=True)
    class Meta:
        model=Video
        fields=['author','caption','video','uploaded_at']
        
class VideoCommentSerializers(serializers.ModelSerializer):
    author=serializers.CharField(source='author.name',read_only=True)
    class Meta:
        model=VideoComment
        fields=['author','comment','commented_on','created_at']
        
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'name','id']
        
class ChatModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ['name', 'receiver', 'messages', 'timestamp', 'room_name']
        

