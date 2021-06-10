from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueTogetherValidator
from BMS.exceptions import CustomException


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        user = instance.user

        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        # its must be justify as each fist name and last name through the name
        instance.save()
        return instance


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise CustomException(message="This user dose not exist",
                                  field="email",
                                  status_code=400)
        if not user.check_password(data['password']):
            raise CustomException(message="UnAuthonticate",
                                  field="password",
                                  status_code=401)

        return data