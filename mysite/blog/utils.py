from django.contrib.auth.models import User


# User authenticating method made to work without hashed passwd.
def own_authenticate(username, password):

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return None
    
    if user.password == password:
        return user
    
    return None


# TODO remove everything but letters, numbers, -, _
def slugify(title):
    return str(title).lower().replace(' ', '-')