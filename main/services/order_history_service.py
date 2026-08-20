from main.models import OrderStatusHistory


class OrderHistoryService:

    @staticmethod
    def create(

        order,

        old_status,

        new_status,

        user=None,

        note="",

    ):

        return OrderStatusHistory.objects.create(

            order=order,

            old_status=old_status,

            new_status=new_status,

            changed_by=user,

            note=note,

        )