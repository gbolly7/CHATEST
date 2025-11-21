from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ChatRoom, Participant, Message
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .api.serializers import ChatroomSerializers, MessageSerializer, ParticipantSerializer
from rest_framework import serializers


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatroomSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return ChatRoom.objects.all()
    
    def perform_create(self, serializer):
        chatroom = serializer.save()
        # Add the creator as a participant
        Participant.objects.create(user=self.request.user, chatroom=chatroom)

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """Create a new conversation/chatroom with the current user as participant"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            chatroom = serializer.save()
            # Add creator as participant
            Participant.objects.create(user=request.user, chatroom=chatroom)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        chatroom = self.get_object()
        participants = chatroom.participants.all()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a user to a chatroom"""
        chatroom = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        participant, created = Participant.objects.get_or_create(user=user, chatroom=chatroom)
        if created:
            return Response({'message': f'{user.username} added to chatroom'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'User already in chatroom'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a chatroom"""
        chatroom = self.get_object()
        messages = chatroom.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Message.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

