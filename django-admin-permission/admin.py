class AddProhibitionAdminMixin:
    """Prohibition for add in admin"""

    def has_add_permission(self, request, obj=None):  # NOQA
        return False


class DeleteProhibitionAdminMixin:
    """Prohibition for delete in admin"""

    def has_delete_permission(self, request, obj=None):  # NOQA
        return False


class ChangeProhibitionAdminMixin:
    """Prohibition for change in admin"""

    def has_change_permission(self, request, obj=None):  # NOQA
        return False


class AddDeleteProhibitionAdminMixin(AddProhibitionAdminMixin, DeleteProhibitionAdminMixin):
    """Permission on adding and deleting records for admins"""


class ReadOnlyAdminMixin(AddDeleteProhibitionAdminMixin, ChangeProhibitionAdminMixin):
    """Read only admin mixin"""
