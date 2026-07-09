from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.views.generic import ListView, DeleteView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from dashboard.mixins import RoleRequiredMixin
from main.models import Order
from django.contrib import messages
from dashboard.forms import (

    UserUpdateForm,

    ProfileUpdateForm,

)
from django.urls import reverse_lazy

from django.views.generic import UpdateView


from main.utils import create_activity

class UserListView(LoginRequiredMixin,
    RoleRequiredMixin,ListView):
    allowed_roles = [
        "admin",
        "manager",
    ]

    model = User

    template_name = "dashboard/users/list.html"

    context_object_name = "users"

    paginate_by = 20

    def get_queryset(self):

        queryset = (
            User.objects
            .annotate(
                orders_count=Count("orders"),
                total_spent=Sum("orders__total_price")
            )
            .order_by("-date_joined")
        )

        search = self.request.GET.get("search")

        if search:

            queryset = queryset.filter(

                Q(username__icontains=search) |

                Q(first_name__icontains=search) |

                Q(last_name__icontains=search) |

                Q(email__icontains=search)

            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["total_users"] = User.objects.count()

        context["staff_users"] = User.objects.filter(
            is_staff=True
        ).count()

        context["active_users"] = User.objects.filter(
            is_active=True
        ).count()

        context["search"] = self.request.GET.get(
            "search",
            ""
        )

        return context

from django.db.models import Sum

class UserDetailView(LoginRequiredMixin,
    RoleRequiredMixin,DetailView):
    allowed_roles = [
        "admin",
        "manager",
    ]

    model = User

    template_name = "dashboard/users/detail.html"

    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.object

        orders = Order.objects.filter(user=user)

        context["orders"] = orders.order_by("-created_at")[:5]

        context["orders_count"] = orders.count()

        context["pending_count"] = orders.filter(
            status="Pending"
        ).count()

        context["delivered_count"] = orders.filter(
            status="Delivered"
        ).count()

        context["cancelled_count"] = orders.filter(
            status="Cancelled"
        ).count()

        context["spent"] = (
                orders.aggregate(total=Sum("total_price"))["total"] or 0
        )

        return context

class UserUpdateView(LoginRequiredMixin,
    RoleRequiredMixin,UpdateView):
    allowed_roles = [
        "admin",

    ]

    model = User

    form_class = UserUpdateForm

    template_name = "dashboard/users/edit.html"

    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.POST:

            context["profile_form"] = ProfileUpdateForm(

                self.request.POST,

                self.request.FILES,

                instance=self.object.profile

            )

        else:

            context["profile_form"] = ProfileUpdateForm(

                instance=self.object.profile

            )

        return context

    def form_valid(self, form):

        context = self.get_context_data()

        profile_form = context["profile_form"]

        if profile_form.is_valid():

            self.object = form.save()

            profile_form.save()

            create_activity(

                self.request.user,

                "user_updated",

                f'User "{self.object.username}" updated.'

            )

            messages.success(

                self.request,

                "User updated successfully."

            )

            return redirect(

                "user_detail",

                pk=self.object.pk

            )

        return self.render_to_response(context)

    def get_success_url(self):

        return reverse_lazy(

            "user_detail",

            kwargs={

                "pk": self.object.pk

            }

        )



class UserDeleteView(LoginRequiredMixin,
    RoleRequiredMixin, DeleteView):
    allowed_roles = [
        "admin",
    ]

    model = User

    template_name = "dashboard/users/delete.html"

    context_object_name = "user_obj"

    success_url = reverse_lazy("user_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "User deleted successfully."
        )

        return super().form_valid(form)