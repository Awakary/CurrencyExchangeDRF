from rest_framework import serializers


class CustomErrorSerializer(serializers.Serializer):

    @property
    def errors(self) -> dict:
        """Переопределение ошибок"""

        validation_errors = super().errors
        for field, errors in validation_errors.items():
            return {"message": f"Поле: {field} - {errors[0]}"}
