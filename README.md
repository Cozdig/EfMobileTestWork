# Система аутентификации и авторизации

## Описание проекта

Backend-приложение с собственной системой аутентификации и авторизации, реализующей разграничение прав доступа на основе ролей и разрешений (RBAC). Права доступа хранятся в базе данных и управляются через API администратором.

## Технологии

- Python 3.12
- Django 5.x
- Django REST Framework (DRF)
- djangorestframework-simplejwt (JWT аутентификация)
- PostgreSQL

## Установка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>
cd TestWork

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Применение миграций
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера
python manage.py runserver
```
### 1. Общая концепция

Система реализует ролевую модель доступа (Role-Based Access Control) с гибким управлением правами через базу данных. В отличие от жестко зашитых прав, администратор может динамически изменять разрешения для каждой роли без изменения кода.

### 2. Схема базы данных

#### Таблица `users_customuser` (пользователи)

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | AutoField | PRIMARY KEY | Уникальный идентификатор |
| email | EmailField | UNIQUE, NOT NULL | Логин пользователя |
| first_name | CharField(30) | NOT NULL | Имя |
| last_name | CharField(50) | NOT NULL | Фамилия |
| patronymic | CharField(40) | NULL | Отчество |
| role | CharField(20) | NOT NULL | Роль (admin/manager/user) |
| password | CharField(128) | NOT NULL | Хэш пароля |
| is_active | BooleanField | DEFAULT=True | Активен ли аккаунт |
| is_superuser | BooleanField | DEFAULT=False | Суперпользователь |
| is_staff | BooleanField | DEFAULT=False | Персонал |
| last_login | DateTimeField | NULL | Последний вход |
| date_joined | DateTimeField | DEFAULT=now | Дата регистрации |

#### Таблица `users_permission` (разрешения)

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | AutoField | PRIMARY KEY | Уникальный идентификатор |
| codename | CharField(100) | UNIQUE, NOT NULL | Код разрешения |
| name | CharField(255) | NOT NULL | Человекочитаемое название |

#### Таблица `users_rolepermission` (права ролей)

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | AutoField | PRIMARY KEY | Уникальный идентификатор |
| role | CharField(20) | NOT NULL | Роль (admin/manager/user) |
| permission | ForeignKey | ON DELETE CASCADE | Ссылка на Permission |

**Уникальное ограничение:** `(role, permission)` - одной роли нельзя дважды выдать одно право

### 3. Правила доступа по умолчанию

| Разрешение | admin | manager | user |
|------------|-------|---------|------|
| can_view_product | ✅ | ✅ | ✅ |
| can_create_product | ✅ | ✅ | ❌ |
| can_edit_product | ✅ | ✅ | ❌ |
| can_delete_product | ✅ | ❌ | ❌ |
| can_view_user | ✅ | ✅ | ❌ |
| can_edit_user | ✅ | ❌ | ❌ |
| can_delete_user | ✅ | ❌ | ❌ |
| can_manage_roles | ✅ | ❌ | ❌ |
