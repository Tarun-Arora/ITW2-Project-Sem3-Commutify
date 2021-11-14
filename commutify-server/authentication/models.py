from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.

class ChatMessageManager(models.Manager):
    def by_chat(self, chat):
        qs = msg.objects.filter(chat_room=chat).order_by("-dttime")
        return qs


class msg(models.Model):
    sender_id = models.ForeignKey('UserInfo', on_delete=CASCADE)
    dttime = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=1024)
    chat_room = models.ForeignKey('Chat', on_delete=CASCADE)
    objects = ChatMessageManager()

    def __str__(self):
        return self.message


class Chat(models.Model):
    msgs = models.ManyToManyField(msg, related_name='listmsgs', blank=True)
    users = models.ManyToManyField('UserInfo')
    title = models.CharField(max_length=255, unique=True, blank=False)

    def __str__(self):
        return self.title

    def connect_user(self, user):
        if not user in self.users.all():
            self.users.add(user)
            self.save()
        return True

    def dissconnect_user(self, user):
        if user in self.users.all():
            self.users.remove(user)
            self.save()
        return True

    @property
    def group_name(self):
        return f"Chat-{self.id}"



class UserInfo(AbstractUser):
    groups = models.ManyToManyField('Group', related_name='groups', blank=True)
    status = models.CharField(max_length=256, default='Start', blank=True)
    dob = models.DateField(null=True)
    friends = models.ManyToManyField('Friend', blank=True)
    friend_requests = models.ManyToManyField('UserInfo', blank=True, default=None)
    group_requests = models.ManyToManyField('Group', blank=True, default=None)
    verify_pin = models.IntegerField(null=True)
    is_verified = models.BooleanField(default=False)

class Friend(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=CASCADE)
    chats = models.ForeignKey(Chat, on_delete=CASCADE)

class Group(models.Model):
    members = models.ManyToManyField(UserInfo, related_name='members', blank=True)
    admins = models.ManyToManyField(UserInfo, related_name='admins')
    description = models.CharField(max_length=256, default='')
    name = models.CharField(max_length=32, default='')
    groupDP = models.ImageField(null=True, blank=True)
    chats = models.ForeignKey(Chat, on_delete=CASCADE, blank=True, null=True)

class ForgotPwdRequest(models.Model):
    email = models.EmailField()
    sttime = models.DateTimeField(auto_now=True)
    otp = models.IntegerField()


class Image(models.Model):
    name = models.CharField(max_length=500)
    img_url = models.URLField(default=None)