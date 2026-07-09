from django.core.exceptions import PermissionDenied


def has_role(user, roles):
    """
    Foydalanuvchining berilgan rollardan biriga egaligini tekshiradi.
    Superuser har doim ruxsat oladi.
    """

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if not hasattr(user, "profile"):
        return False

    return user.profile.role in roles


def role_required(*roles):
    """
    Function Based View uchun decorator.
    """

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if not has_role(request.user, roles):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator