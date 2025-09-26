from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

# --- Custom serializer for login with email ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            
            # Ajouter des informations utilisateur supplémentaires
            user = self.user
            data['user'] = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': f"{user.first_name} {user.last_name}".strip(),
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
            
            # Ajouter les groupes
            data['user']['groups'] = list(user.groups.values_list('name', flat=True))
            
            return data
            
        except Exception:
            raise serializers.ValidationError(
                {"detail": "Identifiants invalides. Vérifiez votre email et mot de passe."}
            )

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Ajouter des claims personnalisés au token
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        
        return token


# --- Serializer for registration ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un compte avec cet email existe déjà.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password_confirm": "Les mots de passe ne correspondent pas."
            })
        
        attrs.pop('password_confirm')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Assign default group 'Client'
        try:
            client_group = Group.objects.get(name='Client')
            user.groups.add(client_group)
        except Group.DoesNotExist:
            # Si le groupe Client n'existe pas, continuer sans erreur
            pass
            
        return user


# --- Serializer for user details ---
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, 
        slug_field='name', 
        read_only=True
    )
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'groups', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'email', 'is_staff', 'date_joined']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# --- Serializer for user profile update ---
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_first_name(self, value):
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return value.strip() if value else value

    def validate_last_name(self, value):
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return value.strip() if value else value


# --- Serializer for assigning group by admin/manager ---
class AdminAssignGroupSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        many=True,
        required=True
    )
    current_groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True,
        source='groups'
    )

    class Meta:
        model = User
        fields = ['groups', 'current_groups']

    def validate_groups(self, value):
        if not value:
            raise serializers.ValidationError("Au moins un groupe doit être sélectionné.")
        return value

    def update(self, instance, validated_data):
        groups = validated_data.get('groups', [])
        instance.groups.set(groups)
        instance.save()
        return instance


# --- Serializer for admin user management ---
class AdminUserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name', 'groups',
            'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# --- Serializer for password change ---
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        return value

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password_confirm": "Les nouveaux mots de passe ne correspondent pas."
            })
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user