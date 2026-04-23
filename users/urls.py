from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, AdminUserListView, AdminRoleChangeView, PermissionListView, \
    RolePermissionView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin/users/<int:user_id>/role/', AdminUserListView.as_view(), name='change_role'),
    path('admin/assign-role/', AdminRoleChangeView.as_view(), name='assign_role'),
    path('admin/permissions/', PermissionListView.as_view(), name='permissions'),
    path('admin/role-permissions/', RolePermissionView.as_view(), name='role_permissions'),
    path('admin/role-permissions/<str:role_name>/', RolePermissionView.as_view(), name='role_permissions_detail')
]