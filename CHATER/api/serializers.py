from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from CHATER.models import ChatRoom, Message, Participant


User= get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        
class MessageSerializer(ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'chatroom', 'sender', 'text', 'created')
        
class ParticipantSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Participant
        fields = ('id', 'user', 'chatroom', 'joined_at')
        
class ChatroomSerializers(ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'group', 'description', 'updated', 'created', 'participants', 'messages')
        
    def create(self, validated_data):
        chatroom = ChatRoom.objects.create(**validated_data)
        return chatroom
    
