from rest_framework import serializers

from .models import User, Permission, Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class PermissionRelatedField(serializers.StringRelatedField):
    def to_representation(self, value): #when I get the roles
        return PermissionSerializer(value).data

    def to_internal_value(self, data): #when I store the roles
        return data


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(many=True)

    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permissions.add(*permissions)
        instance.save()
        return instance


class RoleRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return RoleSerializer(instance).data

    def to_internal_value(self, data):
        return self.queryset.get(pk=data)


class UserSerializer(serializers.ModelSerializer):
    role = RoleRelatedField(many=False, queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {  # when I register user and get back the response I hidden password
            'password': {'write_only': True}
        }

    def create(self, validated_data):  # password is inside validated_data as other fields first name, last name...
        password = validated_data.pop('password', None)
        instance = self.Meta.model(
            **validated_data)  # this operation will save first name, last name, and email as dictionary
        if password is not None:
            instance.set_password(password)  # hash password in db when new user created
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     password = validated_data.pop('password', None)
    #     if password is not None:
    #         instance.set_password(password)  # hash password in db when new user created
    #     instance.save()
    #     return instance
