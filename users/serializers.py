from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'is_staff', 'password', 'is_active']
        read_only_fields = ['id', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, password):
        try:
            validate_password(password, self.instance)
        except DjangoValidationError as err:
            raise serializers.ValidationError(err.messages)

    def to_representation(self, user):
        data = super().to_representation(user)
        if 'password' in data:
            del data['password']
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'first_name', 'last_name', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login', 'id', 'is_staff']


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def validate_password(self, password):
        try:
            validate_password(password, self.instance)
        except DjangoValidationError as err:
            raise serializers.ValidationError(err.messages)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
