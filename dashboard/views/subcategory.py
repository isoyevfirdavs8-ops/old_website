from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from main.models import (
    SubCategory,
    Category,
)

from dashboard.forms import SubCategoryForm
from main.utils import create_activity


class SubCategoryListView(ListView):

    model = SubCategory

    template_name = "dashboard/subcategory/list.html"

    context_object_name = "subcategory"

    paginate_by = 15

    def get_queryset(self):

        queryset = (

            SubCategory.objects

            .select_related("category")

            .annotate(

                products_count=Count("products")

            )

            .order_by("category__name", "name")

        )

        search = self.request.GET.get("search")

        category = self.request.GET.get("category")

        if search:

            queryset = queryset.filter(

                Q(name__icontains=search) |

                Q(name_ru__icontains=search)

            )

        if category:

            queryset = queryset.filter(

                category_id=category

            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.order_by("name")

        context["selected_category"] = self.request.GET.get(

            "category",

            ""

        )

        context["search"] = self.request.GET.get(

            "search",

            ""

        )

        context["total_subcategories"] = SubCategory.objects.count()

        context["total_products"] = sum(

            x.products_count

            for x in context["subcategory"]

        )

        return context


class SubCategoryDetailView(DetailView):

    model = SubCategory

    template_name = "dashboard/subcategory/detail.html"

    context_object_name = "subcategory"


class SubCategoryCreateView(CreateView):

    model = SubCategory

    form_class = SubCategoryForm

    template_name = "dashboard/subcategory/create.html"

    success_url = reverse_lazy("subcategory_list")

    def form_valid(self, form):

        response = super().form_valid(form)

        create_activity(

            self.request.user,

            "subcategory_created",

            f'SubCategory "{self.object.name}" created.'

        )

        messages.success(

            self.request,

            "SubCategory created successfully."

        )

        return response


class SubCategoryUpdateView(UpdateView):

    model = SubCategory

    form_class = SubCategoryForm

    template_name = "dashboard/subcategory/edit.html"

    context_object_name = "subcategory"

    def form_valid(self, form):

        response = super().form_valid(form)

        create_activity(

            self.request.user,

            "subcategory_updated",

            f'SubCategory "{self.object.name}" updated.'

        )

        messages.success(

            self.request,

            "SubCategory updated successfully."

        )

        return response

    def get_success_url(self):

        return reverse_lazy(

            "subcategory_detail",

            kwargs={

                "pk": self.object.pk

            }

        )


class SubCategoryDeleteView(DeleteView):

    model = SubCategory

    template_name = "dashboard/subcategory/delete.html"

    success_url = reverse_lazy("subcategory_list")

    context_object_name = "subcategory"

    def form_valid(self, form):

        create_activity(

            self.request.user,

            "subcategory_deleted",

            f'SubCategory "{self.object.name}" deleted.'

        )

        messages.success(

            self.request,

            "SubCategory deleted."

        )

        return super().form_valid(form)