from django.contrib import admin


class PermissionAddDeleteAdminMixin(admin.ModelAdmin):
    """Mixin for permission add and delete object in admin interface"""

    def has_add_permission(self, request, obj=None):
        """Overridden `has_add_permission` method to prevent the user in the
         administrator panel to create an entry if the object has already been created."""

        return False if self.model.get_object() else True

    def has_delete_permission(self, request, obj=None):
        """Overridden method `has_add_permission` to prevent a user in the
         admin panel can delete entries."""

        return False
