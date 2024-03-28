from django.shortcuts import render, redirect
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import own_authenticate, slugify
from .models import Article
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
#from django.contrib.auth.forms import UserCreationForm


@csrf_exempt #with this annotation post request can be made w/o csrf token. Fixed by removing this and adding token to html.
def signin_view(request):
    """Handles requests sent to sign in url (login/).
    Logs user in if correct information is given.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.

    Returns
    -------
    HttpResponse
        if method is GET renders login.html
    HttpResponse
        if method is POST and authentication is successful redirects to home page.
    HttpResponse
        if method is POST and authentication is unsuccessful reloads login page.
    """

    if request.method == 'POST':

        if request.POST.get('username'):

            username = request.POST['username']
            password = request.POST['pwd']

            # I wrote own authentication method to work with unsafe password storing.
            user = own_authenticate(username=username, password=password)
            """
            Use this with fixed password hashing to authenticate user.
            
            user = authenticate(username=username, password=password)
            """

            if user is not None:
                login(request, user)
                return redirect('home')
            
            else:
                messages.error(request, "Incorrect account information!")
        else:
            return redirect('login')

    return render(request, 'login.html')


def signup_view(request):
    """Handles requests sent to registering url (register/).
    Creates new user object and saves it into database if information given is correct.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.

    Returns
    -------
    HttpResponse
        if method is GET renders register.html
    HttpResponse
        if method is POST and saving user is successful redirects to registering confirmed page.
    HttpResponse
        if method is POST and saving user is unsuccessful re renders registering page.
    """

    if request.method == 'POST' and request.POST.get('username') and request.POST.get('pwd'):
        
        # This does not hash password and allows it to be retreived in clear text.
        user = User(username=request.POST['username'], password=request.POST['pwd']) # Create user object.
        """
        Under is properly hashed password to fix issue of retreiving passwords.
        
        user = User.objects.create_user(request.POST['username'], request.POST['pwd'])
        """

        try: # If username is taken exception is raised.
            user.save() # Create new row for user object into database

        except IntegrityError:
            messages.error(request, "Username already taken!")
            return render(request, 'register.html')
        
        #return render(request, 'regcomp.html')
        return redirect('registered') #Loads confirmation page
    else:
        messages.error(request, "Invalid inputs!")
    """
    With this execution of sign up method we can use djangos password validators automatically.
    This way password is hashed properly. Using this form also fixes problem above.

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registered')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
    """
    
    return render(request, 'register.html')


def show_registered(request):
    """Handles requests sent to registering confirmation url (registered/).
    Gives options to redirect into differend pages after registering new User.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.

    Returns
    -------
    HttpResponse
        if method is GET renders regcomp.html
    HttpResponse
        if method is POST and form1_id equals log redirects to login url.
    HttpResponse
        if method is POST and form2_id equals front redirects to home url.
    """

    if request.method == 'POST':

        if request.POST['form1_id'] == 'log':
            return redirect('login')
        
        if request.POST['form2_id'] == 'front':
            return redirect('')
        
    return render(request, "regcomp.html")


def sign_out(request):
    """Handles requests sent to log out url (logout/).
    Performs logging out and redirects to home page.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.

    Returns
    -------
    HttpResponse
        Redirects to home url.
    """

    logout(request)

    request.user = AnonymousUser()

    return redirect('home') # Use name parameter for redirect!


def show_article_titles(request):
    """Handles requests sent to home page url (/).
    Performs loading index.html and retreiving articles from database.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.

    Returns
    -------
    HttpResponse
        Renders index.html.
    """
    articles = Article.objects.all().order_by('date') # table name is blog_article

    return render(request, 'index.html', {'articles':articles, 'username':request.user.username})


def show_article_details(request, slug):
    """Handles requests sent to custom articles url (r'^(?P<slug>[\w-]+)/$').
    Renders page that shows full article and gives option for redirecting.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.
    slug : str
        Slug attribute from article that is wanted to be shown.

    Returns
    -------
    HttpResponse
        if method is GET renders article_detail.html
    HttpResponse
        if method is POST redirects to article_edit url.
    """

    # This is unsafe query where input is not sanitized. If slug parameter is modified externally injecting query is possible.
    query = "SELECT * FROM blog_article WHERE slug='" + slug + "'"
    articles = list(Article.objects.raw(query))[:1]
    article = articles[0]
    """
    To fix this issue use djangos inbuild querysets. Those sanitize input automatically.

    article = Article.objects.get(slug=slug)
    """

    if request.method == 'POST':
        """
        This fixes possibility to send post request to correct url without button.
        perhaps not needed im not sure.

        if request.user.username != article.author.username:
            return redirect(reverse('article_details', kwargs={'slug': slug}))
        """
        # If edit button is pressed, redirect to editing url and take slug with redirect.
        return redirect(reverse('article_edit', kwargs={'slug': slug}))
    
    return render(request, 'article_detail.html', {'article': article})


# Horisontal access elevation here and possibly vertical as well.
# @login_required(login_url='login') This fixes vertical elevation.
def show_article_edit(request, slug):
    """Handles requests sent to custom articles editing url (r'^(?P<slug>[\w-]+)/edit/$').
    Renders page that shows article fields in text areas and gives option for redirecting.
    Saves changes made into article into database.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.
    slug : str
        Slug attribute from article that is wanted to be shown.

    Returns
    -------
    HttpResponse
        if method is GET renders article_edit.html
    HttpResponse
        if method is POST redirects to article_details url.
    """
    # Retreives article from database that matches slug.
    article = Article.objects.get(slug=slug)
    """
    This fixes horizontal and vertical access elevation. 
    If username is not correct redirection back to details page.

    if request.user.username != article.author.username:
        return redirect(reverse('article_details', kwargs={'slug': slug}))
    """
    if request.method == 'POST':

        # If method is post then save changes made to article.
        article.title = request.POST['title']
        article.body = request.POST['article_body']
        article.slug = slugify(article.title)
        article.save()

        # redirect to article detail page and take slug with redirect.
        return redirect(reverse('article_details', kwargs={'slug': article.slug}))
    
    return render(request, 'article_edit.html', {'article': article})


@login_required(login_url='login')
def create_article_view(request):
    """Handles requests sent to articles creating url (create/).
    Renders page that shows article fields in text areas and gives option for redirecting.
    Creates new Article object and saves it into database.

    Parameters
    ----------
    request : HttpRequest
        Includes all request information.

    Returns
    -------
    HttpResponse
        Renders create_article.html
    """
    if request.method == 'POST':

        # Some input sanitation should be done for title and body to prevent xss!
        try: # A bit dumb but works.

            if request.POST['title'] != None or request.POST['title'] != '':
                title = request.POST['title']
                body = request.POST['article_body']
                slug = slugify(title)
                author = request.user
                article = Article(title=title, body=body, slug=slug, author=author)
                article.save()

        except:
            pass

    user = request.user
    articles = Article.objects.filter(author=user)

    return render(request, 'create_article.html', {'username':request.user.username, 'articles':articles})
