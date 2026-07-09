from django.http import JsonResponse
from django.views import View

from main.models import Notification


class NotificationAPIView(View):

    def get(self, request):

        if not request.user.is_authenticated:

            return JsonResponse(
                {
                    "count": 0,
                    "notifications": []
                }
            )

        notifications = (
            Notification.objects
            .filter(user=request.user)
            .order_by("-created_at")[:5]
        )

        data = []

        for item in notifications:

            data.append({

                "id": item.id,

                "title": item.title,

                "message": item.message,

                "time": item.created_at.strftime("%d %b %H:%M"),

                "read": item.is_read

            })

        return JsonResponse({

            "count": Notification.objects.filter(
                user=request.user,
                is_read=False
            ).count(),

            "notifications": data

        })



class NotificationReadView(View):

    def post(self, request, pk):

        if not request.user.is_authenticated:

            return JsonResponse(
                {
                    "success": False
                },
                status=403
            )

        try:

            notification = Notification.objects.get(

                id=pk,

                user=request.user

            )

        except Notification.DoesNotExist:

            return JsonResponse(
                {
                    "success": False
                },
                status=404
            )

        notification.is_read = True

        notification.save()

        unread = Notification.objects.filter(

            user=request.user,

            is_read=False

        ).count()

        return JsonResponse({

            "success": True,

            "count": unread

        })