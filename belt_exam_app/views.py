from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Count


def index(request):
    return render(request, "login.html")

def createUser(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            print("User's password entered was " + request.POST['password'])
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(name=request.POST['name'], password=hashed_pw, email=request.POST['email'])
            print("User's password has been changed to " + user.password)
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_name = User.objects.filter(name=request.POST['name'])
        if users_with_name:
            user = users_with_name[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id #IMPORTANT!!!
                return redirect('/welcome')
            else:
                print("Password didn't match")
                messages.error(request, "Incorrect name or password")
        else:
            print("Name not found")
            messages.error(request, "Incorrect name or password")
    return redirect('/')

def welcome(request):
    if "user_id" in request.session:
        context = {
        "all_quotes": Quote.objects.all(),
        "user": User.objects.get(id=request.session['user_id']),
        "all_likes": Quote.objects.annotate(likes=Count('users_who_like_quote')).order_by('-likes'),
    }
        return render(request, "welcome.html", context)
    else:
        return redirect('/')

def addQuote(request):
    if request.method == "POST":
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            Quote.objects.create(
            quote=request.POST["quote"],
            author=request.POST["author"],
            user = User.objects.get(id=request.session['user_id'])
            )
    return redirect('/welcome')

def deleteQuote(request, id):
    if request.method == "POST":
        quote_with_id = Quote.objects.filter(id=id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            if quote.user == user:
                quote.delete()
    return redirect('/welcome')

def likeQuote(request, id):
    if request.method == "POST":
        quote_with_id = Quote.objects.filter(id=id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            quote.users_who_like_quote.add(user)
    return redirect('/welcome')

def unlikeQuote(request, id):
    if request.method == "POST":
        quote_with_id = Quote.objects.filter(id=id)
        if quote_with_id:
            quote = quote_with_id[0]
            user = User.objects.get(id=request.session['user_id'])
            quote.users_who_like_quote.remove(user)
            #user.cats_voted_for.remove(cat)
    return redirect('/homepage')

def displayUser(request, id):
    context = {
        "user": User.objects.get(id=id)
    }
    return render(request, "user_quotes.html", context)

def editUser(request, id):
    context = {
        "user": User.objects.get(id=id)
    }
    return render(request, "edit_user.html", context)

def submitUser(request, id):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
    user = User.objects.get(id=id)
    if request.POST["name"]:
        user.name = request.POST["name"]
    if request.POST["email"]:
        user.email = request.POST["email"]
    user.save()
    return redirect(f'/myaccount/edit/{user.id}')


# def userProfile(request):
#     context = {
#         "user": User.objects.get(id=request.session['user_id'])
#     }
#     return render(request, "edit_user.html", context)

def logout(request):
    request.session.clear()
    messages.info(request, "Logged out successfully!")
    return redirect('/')