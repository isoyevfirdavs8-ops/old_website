from django.db import models


class OrderManager(models.Manager):

    def pending(self):
        return self.filter(
            status="Pending"
        )

    def processing(self):
        return self.filter(
            status="Processing"
        )

    def delivered(self):
        return self.filter(
            status="Delivered"
        )

    def cancelled(self):
        return self.filter(
            status="Cancelled"
        )