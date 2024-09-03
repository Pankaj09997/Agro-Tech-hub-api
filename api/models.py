from typing import Iterable
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.utils import timezone



class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            
            name=name,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.TextField(default='Guest')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Post(models.Model):
    # means that each post is associated with the user which helps in creating one to many relationship
    
    author = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    content=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to='post_images',blank=True,null=True)
    pdf=models.FileField(upload_to='pdf_files',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    # this method is used for validation of the post if they are correctly posted or not
    def clean(self):
        if not self.content and not self.image and not self.pdf:
            raise ValidationError("You cannnot post empty field")
         
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self) :
        return f'Post by {self.author.name} on {self.created_at}'
    
class Comment(models.Model):

    comment = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    commented_on = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f'comment by {self.author.name} on {self.commented_on.author}'
    
class Video(models.Model):
    caption = models.CharField(default='Video 1', max_length=100)
    video = models.FileField(upload_to='video/%Y/')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)



class VideoComment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    commented_on = models.ForeignKey(Video, on_delete=models.CASCADE)
    commented_at = models.DateTimeField(default=timezone.now)
    
class Chatroom(models.Model):
    user1 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user1',default=1)
    user2 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user2',default=2)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=["user1","user2"],name="unique chatroom")
        ]
        
    def clean(self):
        if self.user1==self.user2:
            raise ValidationError("A User Cannot chat with themselves")
        
    def __str__(self):
        return f"ChatRoom between {self.user1.name} and {self.user2.name} "
        
        
    
class Message(models.Model):
    chat_room = models.ForeignKey(Chatroom, on_delete=models.CASCADE, related_name='chatroom', null=True, blank=True)
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sender',default=3)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by_sender = models.BooleanField(default=False)
    read_by_recipient = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.sender.name}: {self.content} at {self.timestamp}'
    def clean(self):
       if self.sender not in [self.chat_room.user1, self.chat_room.user2]:
        raise ValidationError("Sender must be one of the users in the chatroom")

    def save(self, *args, **kwargs):
        # Run the clean method to validate before saving
         self.full_clean()
         super().save(*args, **kwargs)
        


        



