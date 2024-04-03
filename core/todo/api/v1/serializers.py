from rest_framework import serializers
from ...models import Task
from accounts.models import User


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "done",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = User.objects.get(
            email=self.context.get("request").user.email
        )
        return super().create(validated_data)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("created_date", None)
            rep.pop("updated_date", None)
        else:
            rep.pop("description", None)
        return rep
