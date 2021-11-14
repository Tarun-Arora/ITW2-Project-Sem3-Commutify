from rest_framework import generics, authentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view

from authentication.models import Image
from .serializers import *


class Fr_Request(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Fr_RequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'message': 'Success'})


class Fr_Response(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Fr_ResponseSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'message': 'Success'})


class Fr_Remove(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Fr_RemoveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'message': 'Success'})


class Grp_Request(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Grp_RequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'message': 'Success'})


class Grp_Response(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Grp_ResponseSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'message': 'Success'})


class Grp_Create(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Grp_CreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'id': r})


class Grp_Exit(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = Grp_ExitSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response({'message': 'Success'})


class Make_Admin(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = NewAdminSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class Remove_Admin(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoveAdminSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class Remove_Member(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = RemoveMemberSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class RetrieveMessage(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = RetrieveMessageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        r = serializer.save()
        return Response(r)


class GetFriends(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        friends = user.friends.all()
        data = []
        for fr in friends:
            a1 = fr.chats.msgs.last()
            a = '1970-01-01 00:00:00.430294+00:00' if a1 == None else str(a1.dttime)
            x = [fr.user.username, user.username]
            x.sort()
            room = 'fr-' + str(x[0]) + '-' + str(x[1])
            name = "user_" + str(fr.user.username)
            try:
                img = Image.objects.get(name=name)
                img_url = img.img_url
            except:
                img_url = "https://eitrawmaterials.eu/wp-content/uploads/2016/09/person-icon.png"

            data.append({
                'id': fr.user.id,
                'username': fr.user.username,
                'first_name': fr.user.first_name,
                'last_name': fr.user.last_name,
                'status': fr.user.status,
                'last_act': a,
                'unseen': 0,
                'room': room,
                'img_url': img_url
            })
        data.sort(key=lambda fr: fr['last_act'], reverse=True)
        return Response(data)


class GetGroups(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        groups = user.groups.all()
        data = []
        for gr in groups:
            a1 = gr.chats.msgs.last()
            a = '1970-01-01 00:00:00.430294+00:00' if a1 == None else str(a1.dttime)
            room = 'grp-' + str(gr.id)
            name = "grp_" + str(gr.id)
            try:
                img = Image.objects.get(name=name)
                img_url = img.img_url
            except:
                img_url = "https://www.iconpacks.net/icons/1/free-user-group-icon-296-thumb.png"

            data.append({
                'id': gr.id,
                'name': gr.name,
                'description': gr.description,
                'last_act': a,
                'room': room,
                'unseen': 0,
                'img_url': img_url
            })
        data.sort(key=lambda gr: gr['last_act'], reverse=True)
        return Response(data)


class GetRequests(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        groups = user.group_requests.all()
        data = []
        for gr in groups:
            data.append({
                'id': gr.id,
                'name': gr.name,
                'type': 1,
                'description': gr.description
            })
        friends = user.friend_requests.all()
        for fr in friends:
            data.append({
                'username': fr.username,
                'first_name': fr.first_name,
                'last_name': fr.last_name,
                'type': 0
            })
        return Response(data)

@api_view(('GET',))
def ProfileView(request , username):
    try:
        user = UserInfo.objects.get(username = username)
        return Response({
            "username": user.username,
            "status": user.status,
            "frcount": user.friends.all().count(),
            "fname": user.first_name,
            "lname": user.last_name,
        }, status=200)
    except Exception as e:
        return Response({'info': 'Bad Request'}, status=404)


@api_view(('GET',))
def ProfileImage(request , type, code):
    try:
        if int(type) == 1:
            name = "grp_" + str(code)
        else:
            name = "user_" + str(code)
        img = Image.objects.get(name=name)
        return Response({
            "img_url": img.img_url,
        }, status=200)
    except Exception as e:
        return Response({'info': 'No image found.'}, status=404)

class ProfileUpdate(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileUpdateSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class ProfileImageUpdate(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProfileImageUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class GroupImageUpdate(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupImageUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})

class GroupUpdate(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})

class GroupMemberList(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = GroupMemberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data  = serializer.save()
        return Response(data)


@api_view(('GET',))
def GroupView(request , id):
    try:
        grp = Group.objects.get(id=id)
        return Response({
            "name": grp.name,
            "description": grp.description
        }, status=200)
    except Exception as e:
        return Response({'info': 'Bad Request'}, status=404)