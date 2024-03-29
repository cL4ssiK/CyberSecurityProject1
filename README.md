# Instructions
1. Make sure you have Python and Django installed properly.
2. Download the project to your local machine.
3. Navigate yourself to project root directory (../mysite/).
4. Make following commands:
```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
```

# Using the site
There are 3 accounts present in the application by default.
```
user1 - 123
user2 - 123
admin - admin
```
If you wish to test the flaw 2 do the following:
1. Log in with any user
2. From front page click link to open an article that has published with other account that you are logged in with.
3. Add '/edit/' to the url and press enter key. This should take you to the editing page even though you are not the owner of the article.


