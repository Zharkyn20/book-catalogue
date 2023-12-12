import random
from decouple import config

from django.core.mail import send_mail
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser

redis_client = get_redis_connection()


def start_registration(data):
    """Отправка кода подтверждения на почту и сохранение данных в Redis"""
    
    success = ("Код подтверждения отправлен на вашу почту.", status.HTTP_200_OK)
    error = ("Ошибка при отправке кода подтверждения", status.HTTP_500_INTERNAL_SERVER_ERROR)

    verification_code = generate_verification_code()

    is_code_sent = send_code_to_email(verification_code, data["email"])
    if not is_code_sent:
        return error

    redis_data = get_redis_data(data, verification_code)
    
    is_data_set = set_data_to_redis(redis_data)
    if not is_data_set:
        return error
    
    return success


def generate_verification_code():
    """Генерация кода подтверждения"""
    return random.randint(1000, 9999)


def send_code_to_email(verification_code, email):
    """Отправка кода подтверждения на почту"""
    subject = 'Verify Your Email'
    message = f'Your verification code is {verification_code}'
    from_email = config("SEND_MAIL")
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(e)
        return False
    return True
    

def get_redis_data(data, verification_code):
    """Создание словаря данных о пользователе для сохранения в Redis"""
    redis_data = {
        'email': data["email"],
        'password': data["password"],
        'full_name': data["full_name"],
        'is_author': str(data["is_author"]),
        'verification_code': verification_code,
    }
    return redis_data


def set_data_to_redis(redis_data):
    """Сохранение данных о пользователе в Redis"""
    unique_token = redis_data['email']
    try:
        redis_client.hmset(unique_token, redis_data)
        redis_client.expire(unique_token, 120)
    except Exception as e:
        print(e)
        return False
    return True


def code_verification(data):
    """Проверка кода подтверждения и создание пользователя"""
    email = data['email']
    code = data['code']

    user_details = get_user_details_by_email(email)
    if code == user_details['verification_code']:
        user = create_user(user_details)
        data = get_token_data(user)

    return data, status.HTTP_200_OK


def get_user_details_by_email(email):
    """Получение данных о пользователе из Redis"""
    try:
        user_details = redis_client.hgetall(email)
    except Exception as e:
        print(e)
        return False
    user_details = {key.decode('utf-8'): value.decode('utf-8') for key, value in user_details.items()}
    return user_details


def create_user(data):
    """Создание пользователя"""
    user = CustomUser.objects.create(
        email=data['email'],
        full_name=data['full_name'],
        is_author=data['is_author'],
        is_active=True
    )
    user.set_password(data['password'])
    user.save()
    return user


def get_token_data(user):
    """Получение токена"""
    refresh = TokenObtainPairSerializer.get_token(user)
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return data
