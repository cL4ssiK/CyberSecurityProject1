from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import own_authenticate, slugify
from .models import Article
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse



def signin_view(request):

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

    return render(request=request, template_name='login.html')



def signup_view(request):

    if (request.method == 'POST' and request.POST.get('username') and request.POST.get('pwd')):
        
        # This does not hash password and allows it to be retreived in clear text.
        # This possibly allows injection of sql queries as username. Needs to be sanitised.
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

    return render(request, 'register.html')



def show_registered(request):

    if request.method == 'POST':

        if request.POST['form1_id'] == 'log':
            return redirect('login')
        
        if request.POST['form2_id'] == 'front':
            return redirect('')
        
    return render(request, "regcomp.html")


# Performs logging out.
def sign_out(request):

    logout(request)

    request.user = AnonymousUser()

    return redirect('home') # Use name parameter for redirect!



def show_article_titles(request):

    articles = Article.objects.all().order_by('date')

    return render(request, 'index.html', {'articles':articles, 'username':request.user.username})


# Shows details of an article
def show_article_details(request, slug):

    article = Article.objects.get(slug=slug)

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


# Opens editing window.
# Horisontal access elevation here and possibly vertical as well.
# @login_required(login_url='login') This fixes vertical elevation.
def show_article_edit(request, slug):
    
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


# Selvitä pystyykö julkasun yhteydessä laittaa scriptin tai rikkonaisen kuvan.
# Jos ei voi, niin tee silleen että voi.
@login_required(login_url='login')
def create_article_view(request):

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
