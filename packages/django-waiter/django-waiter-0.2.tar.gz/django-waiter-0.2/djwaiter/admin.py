from django.contrib import admin


class ReadOnlyAdmin():
    extra = 0
    can_delete = False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request, obj=None):
        return False
