from django.contrib import admin

# Register your models here.
from .models import UserInfo, Group, msg, Chat, Friend, ForgotPwdRequest, Image

admin.site.register(UserInfo)
admin.site.register(Group)
admin.site.register(msg)
admin.site.register(Chat)
admin.site.register(Friend)
admin.site.register(ForgotPwdRequest)
admin.site.register(Image)
