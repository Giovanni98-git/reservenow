from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import User
from django.contrib.auth.models import Group

# --- Custom serializer for login with email ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD  # Use email as authentication field

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except Exception:
            raise serializers.ValidationError("Incorrect email or password.")


# --- Serializer for registration ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['pk', 'email', 'password', 'first_name', 'last_name']
        

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # Assign default group 'Client'
        client_group = Group.objects.get(name='Client')
        user.groups.add(client_group)
        return user


# --- Serializer for user details ---
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field='name', read_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'groups']


# --- Serializer for assigning group by admin/manager ---
class AdminAssignGroupSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        write_only=True
    )

    class Meta:
        model = User
        fields = ['group']

    def update(self, instance, validated_data):
        group = validated_data.get('group')
        # Remove all existing groups and assign the new one
        instance.groups.clear()
        instance.groups.add(group)
        instance.save()
        return instance
