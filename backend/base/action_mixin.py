from typing import Any


class MixedPermission:
    """Permission action`s mixin"""

    def get_permission(self) -> list:
        try:
            # Создание экземпляров правил разрешений для соответствующего действия
            permission_classes = [
                permission() for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            # Возвращение стандартного набора правил разрешений,
            # если не найдено специфического для действия
            permission_classes = [permission() for permission in self.permission_classes]
        return permission_classes


class MixedSerializer:
    """Serializers action`s mixin"""

    def get_serializer_class(self) -> Any:
        try:
            return self.serializer_classes_by_action[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class MixedPermissionSerializer(MixedPermission, MixedSerializer):
    """Permission and Serializers action`s mixin"""

    pass
