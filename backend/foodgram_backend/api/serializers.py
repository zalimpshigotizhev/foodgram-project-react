from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password"
        )

    def to_representation(self, instance):
        '''Данная функция помогает скрывать пароль при GET-запросе'''
        #############################################################
        # Если запрос GET, исключаем поле "password"
        if self.context['request'].method == 'GET':
            self.fields.pop('password')
        return super().to_representation(instance)

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
