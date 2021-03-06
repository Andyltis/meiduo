"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import datetime
import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 追加系统导包路径（1.方便注册自应用, 2.修改django认证模型类时，必须以应用名.模型名）
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
# print(sys.path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v((s+hacxqmarb7p0%ne=9$abimtgrrwd^r&car%1vogq#aqcy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'www.meiduo.site', 'api.meiduo.site']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # DRF
    'users.apps.UsersConfig',
    'corsheaders',  # cors
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 最外层的中间件， 先执行
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        "PORT": 3306,
        "USER": "meiduo",
        "PASSWORD": "meiduo123",
        "NAME": "meiduo"
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    "default": {  # 缓存省市区数据
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # 缓存session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_codes": {  # 储存验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# ⽇志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁⽤用已经存在的⽇日志器器
    'formatters': {  # ⽇日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对⽇日志进⾏行行过滤
        'require_debug_true': {  # django在debug模式下才输出⽇日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # ⽇日志处理理⽅方法
        'console': {  # 向终端中输出⽇日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向⽂文件中输出⽇日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/meiduo.log"),  # ⽇日志⽂文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # ⽇日志器器
        'django': {  # 定义了了�个名为django的⽇日志器器
            'handlers': ['console', 'file'],  # 可以同时向终端与⽂文件中输出⽇日志
            'propagate': True,  # 是否继续传递⽇日志信息
            'level': 'INFO',  # ⽇日志器器接收的最低⽇日志级别
        },
    }
}

# DRF配置项

REST_FRAMEWORK = {
    # 异常处理理
    'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.exception_handler',
}

# 修改django认证系统的模型类
AUTH_USER_MODEL = 'users.User'

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://www.meiduo.site:8080',
    'http://api.meiduo.site:8000',
)
CORS_ALLOW_CREDENTIALS = True

# JWT的有效期
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 修改JWT登录视图补充返回值函数
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler',
}

AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]