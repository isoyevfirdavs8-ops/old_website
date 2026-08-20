from django.views.generic import ListView
from django.db.models import Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from dashboard.forms import CategoryForm
from main.utils import create_activity
from main.models import Category
from django.views.generic import DetailView
from main.models import Category, SubCategory, Product
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from dashboard.forms import CategoryForm

from main.utils import create_activity


class CategoryListView(ListView):

    model = Category

    template_name = "dashboard/category/list.html"

    context_object_name = "category"

    paginate_by = 20

    queryset = (

        Category.objects

        .annotate(

            products_count=Count("products"),

            subcategories_count=Count("subcategories")

        )

        .order_by("name")

    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_categories"] = Category.objects.count()

        context["total_products"] = sum(

            c.products_count

            for c in context["category"]

        )

        context["total_subcategories"] = sum(

            c.subcategories_count

            for c in context["category"]

        )

        return context

    def get_queryset(self):
        queryset = (

            Category.objects

            .annotate(

                products_count=Count("products"),

                subcategories_count=Count("subcategories")

            )

            .order_by("name")

        )

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(

                Q(name__icontains=search)

                |

                Q(name_ru__icontains=search)

            )

        return queryset

class CategoryCreateView(CreateView):

    model = Category

    form_class = CategoryForm

    template_name = "dashboard/category/create.html"

    success_url = reverse_lazy("category_list")

    def form_valid(self, form):

        response = super().form_valid(form)

        create_activity(

            self.request.user,

            "category_created",

            f'Category "{self.object.name}" created.'

        )

        messages.success(

            self.request,

            "Category created successfully."

        )

        return response

class CategoryDetailView(DetailView):

    model = Category
    template_name = "dashboard/category/detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        category = self.object

        products = Product.objects.filter(category=category)

        context["products"] = products[:10]
        context["products_count"] = products.count()

        # Endi SubCategory yo'q
        context["subcategories_count"] = 0

        return context



class CategoryDeleteView(DeleteView):

    model = Category

    template_name = "dashboard/category/delete.html"

    success_url = reverse_lazy("category_list")

    def form_valid(self, form):

        create_activity(

            self.request.user,

            "category_deleted",

            f'Category "{self.object.name}" deleted.'

        )

        messages.success(

            self.request,

            "Category deleted successfully."

        )

        return super().form_valid(form)


class CategoryUpdateView(UpdateView):

    model = Category

    form_class = CategoryForm

    template_name = "dashboard/category/edit.html"

    context_object_name = "category"

    def form_valid(self, form):

        response = super().form_valid(form)

        create_activity(

            self.request.user,

            "category_updated",

            f'Category "{self.object.name}" updated.'

        )

        messages.success(

            self.request,

            "Category updated successfully."

        )

        return response

    def get_success_url(self):

        return reverse_lazy(

            "category_detail",

            kwargs={

                "pk": self.object.pk

            }

        )