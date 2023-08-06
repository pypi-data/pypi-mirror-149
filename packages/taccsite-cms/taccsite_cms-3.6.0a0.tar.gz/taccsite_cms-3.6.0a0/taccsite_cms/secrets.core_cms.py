########################
# DATABASE SETTINGS
########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5432',
        'NAME': 'taccsite',
        'USER': 'postgresadmin',
        'PASSWORD': 'taccforever',  # Change before live deployment.
        'HOST': 'core_cms_postgres'
    }
}
