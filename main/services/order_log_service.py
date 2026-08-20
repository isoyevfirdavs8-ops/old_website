from main.models import OrderLog


class OrderLogService:

    @staticmethod
    def create(

        order,

        new_status,

        old_status="",

        user=None,

        comment="",

    ):

        return OrderLog.objects.create(

            order=order,

            old_status=old_status,

            new_status=new_status,

            changed_by=user,

            comment=comment,

        )