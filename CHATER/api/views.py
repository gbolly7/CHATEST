from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/api/ - View all endpoints',
        'GET /api/chatrooms/ - List all chatrooms',
        'POST /api/chatrooms/ - Create a new chatroom',
        'GET /api/chatrooms/:id/ - Get specific chatroom',
        'POST /api/chatrooms/create_conversation/ - Create conversation (alt endpoint)',
        'GET /api/chatrooms/:id/participants/ - Get chatroom participants',
        'POST /api/chatrooms/:id/add_participant/ - Add user to chatroom',
        'GET /api/chatrooms/:id/messages/ - Get chatroom messages',
        'GET /api/messages/ - List all messages',
        'POST /api/messages/ - Create new message',
    ]
    return Response(routes)