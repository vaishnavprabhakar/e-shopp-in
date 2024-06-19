import os
import smtplib
from decouple import config, Csv
from pathlib import Path
import product
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET")
DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '3.92.208.122']
INSTALLED_APPS = [
    'django.contrib.admin',
    'whitenoise.runserver_nostatic',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig', # User app 
    'product.apps.ProductConfig', # Product app
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
]
ROOT_URLCONF = 'eshopy.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'product.context_processors.category_link',
            ],
        },
    },
]
WSGI_APPLICATION = 'eshopy.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB'),
        'USER': config('DBUSER'),
        'PASSWORD': config('PASSWD'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
    }
}
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = '/var/www/staticfiles/' 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = config('EMAILBACKEND')
EMAIL_HOST = config('EMAILHOST')
EMAIL_PORT = int(config('EMAILPORT',cast=int))
EMAIL_USE_TLS = config('EMAILUSE_TLS',cast=bool)
EMAIL_HOST_USER = config('EMAILHOSTUSER')
EMAIL_HOST_PASSWORD = config('EMAILHOSTPASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULTFROMEMAIL')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
TEMPLATES_DIRS = [[BASE_DIR] + STATICFILES_DIRS]
AUTH_USER_MODEL = "user.User"
#-----------------------RAZORPAY PAYMENT GATEWAY-----------------
RAZOR_KEY_ID = config('PAYMENTGATEWAY_ID')
RAZOR_KEY_SECRET = config('KEYSECRET')
# -----------AWS Configuration settings ------------------------------
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = config('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE',cast=bool,default=False)
AWS_DEFAULT_ACL =  config('AWS_DEFAULT_ACL',default=None)
AWS_S3_VERITY = config('AWS_S3_VERITY', cast=bool, default=True)
DEFAULT_FILE_STORAGE = config('DEFAULT_FILE_STORAGE',cast=Csv())