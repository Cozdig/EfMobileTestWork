from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser, Permission, RolePermission
from .permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Пользователь создан',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({'message': 'Аккаунт удален'}, status=204)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Выход выполнен'})
        except Exception:
            return Response({'error': 'Неверный токен'}, status=400)


class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def patch(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            new_role = request.data.get('role')

            if new_role not in ['admin', 'manager', 'user']:
                return Response({'error': 'Неверная роль. Доступны: admin, manager, user'}, status=400)

            user.role = new_role
            user.save()
            return Response({
                'message': f'Роль пользователя {user.email} изменена на {new_role}',
                'user': UserSerializer(user).data
            })
        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)


class AdminRoleChangeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        user_id = request.data.get('user_id')
        role_name = request.data.get('role')

        try:
            user = CustomUser.objects.get(id=user_id)
            if role_name not in ['admin', 'manager', 'user']:
                return Response({'error': 'Неверная роль'}, status=400)

            user.role = role_name
            user.save()
            return Response({'message': f'Роль назначена пользователю {user.email}'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)


class PermissionListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        permissions = Permission.objects.all()
        data = [{'id': p.id, 'codename': p.codename, 'name': p.name} for p in permissions]
        return Response(data)


class RolePermissionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, role_name=None):
        """Получить права роли"""
        if role_name:
            perms = RolePermission.objects.filter(role=role_name)
            data = [{'id': rp.id, 'permission': rp.permission.codename, 'name': rp.permission.name}
                    for rp in perms]
            return Response(data)

        all_roles = ['admin', 'manager', 'user']
        result = {}
        for role in all_roles:
            perms = RolePermission.objects.filter(role=role)
            result[role] = [rp.permission.codename for rp in perms]
        return Response(result)

    def post(self, request):
        role = request.data.get('role')
        permission_id = request.data.get('permission_id')

        if not role or not permission_id:
            return Response({'error': 'Не указана роль или право'}, status=400)

        if role not in ['admin', 'manager', 'user']:
            return Response({'error': 'Неверная роль'}, status=400)

        try:
            permission = Permission.objects.get(id=permission_id)
            RolePermission.objects.get_or_create(role=role, permission=permission)
            return Response({'message': f'Право {permission.codename} добавлено роли {role}'})
        except Permission.DoesNotExist:
            return Response({'error': 'Право не найдено'}, status=404)

    def delete(self, request):
        role = request.data.get('role')
        permission_id = request.data.get('permission_id')

        try:
            role_perm = RolePermission.objects.get(role=role, permission_id=permission_id)
            role_perm.delete()
            return Response({'message': 'Право удалено'})
        except RolePermission.DoesNotExist:
            return Response({'error': 'Право не найдено у этой роли'}, status=404)