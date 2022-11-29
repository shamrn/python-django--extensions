class CreateProhibitionAdminMixin:
    """Prohibition for create object in admin interface"""

    def has_add_permission(self, request, obj=None):  # NOQA
        return False


class DeleteProhibitionAdminMixin:
    """Prohibition for delete object in admin interface"""

    def has_delete_permission(self, request, obj=None):  # NOQA
        return False


class UpdateProhibitionAdminMixin:
    """Prohibition for update object in admin interface"""

    def has_change_permission(self, request, obj=None):  # NOQA
        return False


class CreateAndDeleteProhibitionAdminMixin(CreateProhibitionAdminMixin,
                                           DeleteProhibitionAdminMixin):
    """Prohibition for create and delete object in admin interface"""


class ReadOnlyAdminMixin(CreateAndDeleteProhibitionAdminMixin,
                         UpdateProhibitionAdminMixin):
    """Read only admin mixin"""
