from typing import Any, Optional


class PermissionsMixin:
    def __init__(self, request: Optional[Any] = None, **kwargs):
        super().__init__(**kwargs)
        self.request = request

    @property
    def has_add_permission(self: Any) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.add_{model_name}")

    @property
    def has_change_permission(self: Any) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.change_{model_name}")

    @property
    def has_delete_permission(self: Any) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.delete_{model_name}")

    @property
    def has_view_permission(self: Any) -> bool:
        app_label, model_name = self.model.split(".")
        return self.request.user.has_perm(f"{app_label}.view_{model_name}")
