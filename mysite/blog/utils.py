from django.contrib.auth.models import User


def own_authenticate(username, password):
    """User authenticating method made to work without hashed passwd.

    Parameters
    ----------
        username : str
            Users alleged username
        password : str
            Users alleged password

    Returns
    ------- 
    User
        Correct User object if information is found.

    None 
        if no user information matches parameters.
    """

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return None
    
    if user.password == password:
        return user
    
    return None


# TODO remove everything but letters, numbers, -, _
def slugify(title):
    """Method that creates slug friendly string out of string.

    Parameters
    ----------
        title : str
            String that is modified.

    Returns
    ------- 
    str
        Modified slug.
    """

    return str(title).lower().replace(' ', '-')