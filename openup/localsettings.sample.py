DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'openup_website',                               # Or path to database file if using sqlite3.
        'USER': 'openup',                                       # Not used with sqlite3.
        'PASSWORD': '',                                         # Not used with sqlite3.
        'HOST': 'localhost',                                    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                                         # Set to empty string for default. Not used with sqlite3.
    }
}
