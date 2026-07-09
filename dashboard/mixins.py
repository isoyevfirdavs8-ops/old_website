from django.core.exceptions import PermissionDenied


class RoleRequiredMixin:
    """
    Class Based View uchun Role Mixin
    """

    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            raise PermissionDenied

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, "profile"):
            raise PermissionDenied

        if request.user.profile.role not in self.allowed_roles:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)