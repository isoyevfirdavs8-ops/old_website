from django.db import models


class ProductManager(models.Manager):

    def active(self):
        return self.all()

    def featured(self):
        return self.filter(
            featured=True,
            active=True
        )

    def by_category(self, category_id):
        return self.filter(
            category_id=category_id,
            active=True
        )

    def by_subcategory(self, subcategory_id):
        return self.filter(
            subcategory_id=subcategory_id,
            active=True
        )

    def search(self, query):
        return self.filter(
            title__icontains=query,
            active=True
        )