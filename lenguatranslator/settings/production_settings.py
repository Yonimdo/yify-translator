# SECURITY WARNING: don't run with debug turned on in production!

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = False
ALLOWED_HOSTS = ['localhost', 'lengua-translator.herokuapp.com']

import dj_database_url

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# with open(pyrebase.initialize_app(
#         {
#             "type": "service_account",
#             "project_id": "lengua-b3099",
#             "private_key_id": "932ff237d9d5bde977e4bcf366a1ea7f070ae79a",
#             "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC9PTijMtWSNxf6\nMElIPUfECwdUyYp+s0xqM5qw2XV0Qd1uyU3t3kKrW1JRAeOPUSstY9TJOiqB1XyL\nQctkmtBtdjZD9OM00LUecfoFWp8AmYpQbZBnyZJG3+IoYTAnGVABS54gJ4iNQw8a\n5OWV9pepdW08hLGDLCEg2S6H3fT6gJKJ7HhIqIWG1yfXvuathmmJlPjsUTAvwoXD\nUXZxVqJbskWsmEWJq1BZ5xU4uHhCZ79jR3B9JZ8hUnR41qxIeKUAxOwHUj9P3s11\nyzk4h3QsZ9a/ud+DlqnNxI/dPnfy+xjMX9HiTlsLMOI9qGpnM6oRusefwHutUfAz\nm868ouitAgMBAAECggEAAxyQ/deSidQi4ZfbQwQFVhF7ji1YlaGLgOnwTtAeJxc3\nwnnIFw0vudmUKB871EA/BLQLhg0d/c+6buyNOs5A3X8Zs7knGaTRry2rysK+so46\nJzBmAdusO0Ln8q05n94oSDbFSgoPklZAvVR3yFhE2u7cKPT7/9T0U0uLtFHPlJhy\n89pi94yfgnrv5NH0Y+X3zQjlIZ2/zzFooDCvhiFA4Hkp5Pxlr65m/7b9nmW5hRS7\niKQs2CxZ4HtPspHo+q/eU3gKWLZwEWzHqYjGcvrLnL81wXzp7wOSZUUpbAIH6xHz\ndKff6zl7viDzlKJRu6ZeDKhN8E9mTWbsW/fsZ1FSEQKBgQDudAwpTch2G5Hsn3+3\nr1vX1XRuqVM31bBdoaCIKIlSRkkQdZ3NgXInt7jICVRtCVBpdTppglr7k5Dx76VI\noP04oSlJ2R4p5wm2kbv0qFw0KoFtyWSZX4rKUZzEugntMOyoav9jM1QW+7TWKzrr\nUrymZlhhJWcs9xRt+YExp5pk3wKBgQDLKhVsW7WFp4F75SKUClbsNxj+W2UFDTDM\nVjbLmKETnfQkvV7xE5r4DCMm2FAbqUHC4iWSNHkwkIOzT/xIJRhbC82Q5Zt5+sfo\nWTfAua9KYQQIoVDZo2dVTqXrKyCapp/9KOZ4+GJ4OhTSrgJQnpvcXs3sUYzC1U7D\n3j3f+H738wKBgQDfB6gAUgJ3hd39Bko9EkXDIKGgh7uQc8xcJzqxX8jhLWBVhs0s\nVDDjuVGZuDBBM/8ERGN4IDbdK+7ce5uKzRlLiGHH8s3lv3U0UCcO9RIYsNESUNZJ\nJjX4elE5KBD0y1fvRvTMYkv6mz9POmwHgwF0WjG723IfepKfMkmGmg8s3QKBgQCw\n6Rh2nvVWSSJrrH+LweUnFGNjOlqhJ3dSt9BHQcUhu+2ZAH3oF1ZeoNMLRFmdfKmS\n9jIZOjA9pdnJDuF0QTkQLxr2DbpxYXsqTGZMIGUPs6M7kJ1CpxOYKUA5o/hkMqwm\nWrM2q7OzVYBEZNoHMdYu8y8FlY2pKu3HiYL/wPdvGQKBgHuqoCRESTMVys7a/dTJ\nNQ0Wv2ja9YQyAPzmV2CVN669ugclXJUzhmFTTt0CXEdkJWwQc/A4l3dnnfjjLb3U\nQjHcmqLKY82hGF2MDkzEDlHEVVJ9NDwQbVDWgw832nHOEgWehqwefMOQ0KM+tEVV\nUYNx+ryN98ShKUdQlWphx2s0\n-----END PRIVATE KEY-----\n",
#             "client_email": "firebase-adminsdk-k7ipi@lengua-b3099.iam.gserviceaccount.com",
#             "client_id": "103845936628493993857",
#             "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#             "token_uri": "https://accounts.google.com/o/oauth2/token",
#             "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#             "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-k7ipi%40lengua-b3099.iam.gserviceaccount.com",
#             "apiKey": "apiKey",
#             "authDomain": "projectId.firebaseapp.com",
#             "databaseURL": "https://lengua-b3099.firebaseio.com/",
#             "storageBucket": "gs://lengua-b3099.appspot.com",
#         })) as firebase:
#     pass
