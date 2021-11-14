from django.core.paginator import Paginator
from rest_framework import serializers
from authentication.models import msg, Friend, UserInfo, Group, Chat, Image


class Fr_RequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ['username', ]

    def validate(self, data):
        try:
            user = self.context['request'].user
            requested_to = UserInfo.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid Information")
        m = requested_to.friends.all()
        k = []
        for i in m:
            k.append(i.user)
        if user in k:
            raise serializers.ValidationError("User already friend.")
        elif user in requested_to.friend_requests.all():
            raise serializers.ValidationError("Friend request already send.")
        elif requested_to == user:
            raise serializers.ValidationError("Request to your own username.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        data = self.validated_data
        requested_to = UserInfo.objects.get(username=data['username'])
        requested_to.friend_requests.add(user)
        return self.validated_data


class Fr_ResponseSerializer(serializers.ModelSerializer):
    bool = serializers.BooleanField()
    username = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ['username', 'bool']

    def validate(self, data):
        try:
            user = self.context['request'].user
            responded_to = UserInfo.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if responded_to not in user.friend_requests.all():
            raise serializers.ValidationError("Unauthorized Response.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        data = self.validated_data
        responded_to = UserInfo.objects.get(username=data['username'])
        response = data['bool']
        user.friend_requests.remove(responded_to)
        if int(response) == 1:
            a = [str(user.username), str(responded_to.username)]
            a.sort()
            new_chat = Chat.objects.create(title="fr-" + a[0] + "-" + a[1])
            new_chat.save()
            new_friend = Friend.objects.create(user=responded_to, chats=new_chat)
            new_friend.save()
            new_friend2 = Friend.objects.create(user=user, chats=new_chat)
            new_friend2.save()
            responded_to.friends.add(new_friend2)
            user.friends.add(new_friend)
            new_chat.users.set([user, responded_to])
        return self.validated_data


class Fr_RemoveSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ['username', ]

    def validate(self, data):
        try:
            user = self.context['request'].user
            requested_to = UserInfo.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid Information")
        try:
            a = user.friends.get(user=requested_to)
        except:
            raise serializers.ValidationError("Unauthorized Response.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        data = self.validated_data
        requested_to = UserInfo.objects.get(username=data['username'])
        a = user.friends.get(user=requested_to)
        b = requested_to.friends.get(user=user)
        user.friends.remove(a)
        requested_to.friends.remove(b)
        a.chats.delete()
        return self.validated_data


class Grp_RequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()

    class Meta:
        model = Group
        fields = ['id', 'username']

    def validate(self, data):
        try:
            user = self.context['request'].user
            requested_to = UserInfo.objects.get(username=data['username'])
            grp = Group.objects.get(pk=data['id'])
        except:
            raise serializers.ValidationError({"error": "Invalid username"})
        if user not in grp.admins.all():
            raise serializers.ValidationError("Unauthorized Response.")
        if grp in requested_to.group_requests.all():
            raise serializers.ValidationError({"error": "Group request already send"})
        if requested_to in grp.members.all() or requested_to in grp.admins.all():
            raise serializers.ValidationError({"error": "User already in group."})
        return data


    def save(self, **kwargs):
        user = self.context['request'].user
        data = self.validated_data
        grp = Group.objects.get(pk=data['id'])
        requested_to = UserInfo.objects.get(username=data['username'])
        requested_to.group_requests.add(grp)
        return self.validated_data


class Grp_ResponseSerializer(serializers.Serializer):
    bool = serializers.BooleanField()
    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ['id', 'bool']

    def validate(self, data):
        try:
            user = self.context['request'].user
            grp = Group.objects.get(pk=data['id'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if grp not in user.group_requests.all():
            raise serializers.ValidationError("Unauthorized Response.")
        return data


    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        grp = Group.objects.get(id=data['id'])
        response = data['bool']
        user.group_requests.remove(grp)
        if int(response) == 1:
            grp.members.add(user)
            grp.chats.connect_user(user)
            user.groups.add(grp)
        return self.validated_data


class Grp_CreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    class Meta:
        model = Group
        fields = ['name', 'description', ]

    def validate(self, data):
        try:
            user = self.context['request'].user
        except:
            raise serializers.ValidationError("Invalid Information")
        return data

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        ch = Chat.objects.create()
        ch.save()
        q = Group.objects.create(description=data['description'], name=data['name'], chats=ch)
        ch.title = "grp-" + str(q.id)
        ch.users.set([user])
        ch.save()
        q.admins.set([user])
        q.save()
        user.groups.add(q)
        return q.id


class Grp_ExitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ['id', ]

    def validate(self, data):
        try:
            user = self.context['request'].user
            grp = Group.objects.get(id=data['id'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if user not in grp.admins.all() and user not in grp.members.all():
            raise serializers.ValidationError("Unauthorized Response.")
        return data

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context['request'].user
        grp = Group.objects.get(id=data['id'])
        k = grp.members.all()
        l = grp.admins.all()
        user.groups.remove(grp)
        grp.chats.dissconnect_user(user)
        if user in k:
            grp.members.remove(user)
        else:
            if len(k) + len(l) == 1:
                grp.chats.delete()
            elif len(l) == 1:
                grp.members.remove(k[0])
                grp.admins.set([k[0]])
            else:
                grp.admins.remove(user)
        return self.validated_data


class NewAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=300)
    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ['id', 'username']

    def validate(self, data):
        try:
            req_user = self.context.get('user')
            new_user = UserInfo.objects.get(username=data['username'])
            group = Group.objects.get(id=data['id'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if req_user not in group.admins.all():
            raise serializers.ValidationError("You are not the admin of the group")
        if new_user in group.admins.all():
            raise serializers.ValidationError("User already an admin")
        if new_user not in group.members.all():
            raise serializers.ValidationError("User not added in the group")
        return data

    def save(self):
        new_user = UserInfo.objects.get(username=self.validated_data['username'])
        group = Group.objects.get(id=self.validated_data['id'])
        group.members.remove(new_user)
        group.admins.add(new_user)
        return self.validated_data


class RemoveAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=300)
    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ['id', 'username']

    def validate(self, data):
        try:
            req_user = self.context.get('user')
            new_user = UserInfo.objects.get(username=data['username'])
            group = Group.objects.get(id=data['id'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if req_user not in group.admins.all():
            raise serializers.ValidationError("You are not the admin of the group")
        if new_user not in group.admins.all():
            raise serializers.ValidationError("User is not an admin")
        if req_user == new_user:
            raise serializers.ValidationError("You cannot remove yourself from admin")
        return data

    def save(self):
        new_user = UserInfo.objects.get(username=self.validated_data['username'])
        group = Group.objects.get(id=self.validated_data['id'])
        group.admins.remove(new_user)
        group.members.add(new_user)
        return self.validated_data


class RemoveMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=300)
    id = serializers.IntegerField()

    class Meta:
        model = Group
        fields = ['id', 'username']

    def validate(self, data):
        try:
            req_user = self.context.get('user')
            new_user = UserInfo.objects.get(username=data['username'])
            group = Group.objects.get(id=data['id'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if req_user not in group.admins.all():
            raise serializers.ValidationError("You are not the admin of the group")
        if new_user not in group.members.all() and new_user not in group.admins.all():
            raise serializers.ValidationError("User not added in the group")
        return data

    def save(self):
        new_user = UserInfo.objects.get(username=self.validated_data['username'])
        group = Group.objects.get(id=self.validated_data['id'])
        new_user.groups.remove(group)
        if new_user in group.members.all():
            group.members.remove(new_user)
        else:
            group.admins.remove(new_user)
        return self.validated_data


class RetrieveMessageSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    index = serializers.IntegerField()

    class Meta:
        model = Chat
        fields = ['title', 'index', ]

    def validate(self, data):
        try:
            user = self.context['request'].user
        except:
            raise serializers.ValidationError("Invalid Information")
        try:
            chat = Chat.objects.get(title=data['title'])
        except:
            raise serializers.ValidationError("Invalid Information")
        if user not in chat.users.all():
            raise serializers.ValidationError("Unauthorized Access.")
        return data

    def save(self, **kwargs):
        data = self.validated_data
        chat = Chat.objects.get(title=data['title'])
        index = data['index']
        msg_list = msg.objects.by_chat(chat)
        v = []
        ct=0
        for i in (msg_list):
            if(i.id<index and ct<15):
                v.insert(0,{"id":i.id,"sender": str(i.sender_id), "dttime": i.dttime, "message": str(i.message)})
                ct+=1
        return v

class ProfileUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    fname = serializers.CharField()
    lname = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ['status', 'fname', 'lname']
    
    def validate(self, data):
        user = self.context['user']
        return {'user': user, 'status': data['status'], 'fname': data['fname'], 'lname': data['lname'] }

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        user.status = data['status']
        user.first_name = data['fname']
        user.last_name = data['lname']
        user.save()


class ProfileImageUpdateSerializer(serializers.ModelSerializer):
    img_url = serializers.URLField()

    class Meta:
        model = Image
        fields = ['img_url', ]

    def validate(self, data):
        user = self.context['request'].user
        return {'user': user, 'img_url': data['img_url']}

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']
        name = "user_" + str(user.username)
        try:
            img = Image.objects.get(name=name)
            img.img_url = data['img_url']
            img.save()
        except:
            img = Image.objects.create(name=name, img_url=data['img_url'])
            img.save()


class GroupImageUpdateSerializer(serializers.ModelSerializer):
    img_url = serializers.URLField()
    grp_id = serializers.IntegerField()

    class Meta:
        model = Image
        fields = ['img_url', 'grp_id']

    def validate(self, data):
        user = self.context['request'].user
        try:
            grp = Group.objects.get(id=data['grp_id'])
        except:
            raise serializers.ValidationError("Unauthorized Response.")
        if user not in grp.admins.all() and user not in grp.members.all():
            raise serializers.ValidationError("Unauthorized Response.")
        return {'grp_id': data['grp_id'], 'img_url': data['img_url']}

    def save(self, **kwargs):
        data = self.validated_data
        name = "grp_" + str(data['grp_id'])
        try:
            img = Image.objects.get(name=name)
            img.img_url = data['img_url']
            img.save()
        except:
            img = Image.objects.create(name=name, img_url=data['img_url'])
            img.save()

class GroupUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    description = serializers.CharField()
    name = serializers.CharField()

    class Meta: 
        model = Group
        fields = ['description', 'name', 'id', ]
    
    def validate(self, data):
        try:
            id = data['id']
            group = Group.objects.get(id=id)
        except:
            raise serializers.ValidationError({'err': 'Grp Not Found'})
        user = self.context['request'].user
        if user not in group.admins.all():
            raise serializers.ValidationError("Unauthorized access.")
        return {'group': group, 'description': data['description'], 'name': data['name']}

    def save(self, **kwargs):
        data = self.validated_data
        group = data['group']
        group.description = data['description']
        group.name = data['name']
        group.save()

class GroupMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta: 
        model = Group
        fields = ['id']
    
    def validate(self, data):
        try:
            group = Group.objects.get(pk=data['id'])
        except:
            raise serializers.ValidationError("Invalid Information")
        user = self.context['request'].user
        if user not in group.admins.all() and user not in group.members.all():
            raise serializers.ValidationError("Unauthorized access.")
        return {'group': group}

    def save(self, **kwargs):
        data = self.validated_data
        group = data['group']
        Members = {'members': [], 'admins': [], 'user': []}
        user = self.context['request'].user
        for grMember in group.members.all():
            if grMember == user:
                Members['user'].append(
                    {'username': grMember.username, 'first_name': grMember.first_name, 'last_name': grMember.last_name, 'isAdmin': 0})
                continue
            Members['members'].append({'username': grMember.username, 'first_name': grMember.first_name, 'last_name': grMember.last_name})
        for grMember in group.admins.all():
            if grMember == user:
                Members['user'].append(
                    {'username': grMember.username, 'first_name': grMember.first_name, 'last_name': grMember.last_name, 'isAdmin': 1})
                continue
            Members['admins'].append({'username': grMember.username, 'first_name': grMember.first_name, 'last_name': grMember.last_name})
        return Members