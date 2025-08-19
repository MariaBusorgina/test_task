from rest_framework.response import Response
from rest_framework.views import APIView

from .cache import get_channel_priority
from .tasks import send_message


class SendNotificationView(APIView):
    def post(self, request):
        text = request.data.get("message")
        user_id = request.data.get("user_id")

        channel_priority = get_channel_priority()
        send_message.delay(user_id, text, channel_priority)

        return Response({"status": "queued"})

