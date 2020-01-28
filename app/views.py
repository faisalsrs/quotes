from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Create your views here.


def index(request):
    return render(request, 'index.html')


def logout(request):
    request.session.clear()
    return redirect('/')


def register(request):
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user_in_db = User.objects.filter(email=request.POST['email']).first()

    print('%'*40)
    print(user_in_db)

    if user_in_db:
        messages.error(request, "Invalid credentials")
        return redirect('/')

    hashed_password = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST['fname'],
        last_name=request.POST['lname'],
        email=request.POST['email'],
        password=hashed_password
    )

    request.session['user_id'] = new_user.id

    return redirect('/quotes')


def login(request):
    found_user = User.objects.filter(email=request.POST['email'])
    print('&'*100)
    print(found_user)
    if len(found_user) > 0:
        user_from_db = found_user[0]

        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(),
            user_from_db.password.encode()
        )
        if is_pw_correct:
            request.session['user_id'] = user_from_db.id
            return redirect('/quotes')
    messages.error(request, "Invalid credentials")
    return redirect('/')


def quotes(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')

    context = {
        "user": User.objects.get(id=user_id),
        "all_quotes": Quote.objects.all(),
    }
    return render(request, 'quotes.html', context)


def new_quote(request):
    errors = Quote.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')
    user_posted = User.objects.get(id=user_id)
    Quote.objects.create(
        author=request.POST['author'],
        quote=request.POST['quote'],
        user_related=user_posted
    )
    return redirect('/quotes')


def profile(request, id):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    context = {
        "user": User.objects.get(id=user_id),
    }
    return render(request, 'profile.html', context)


def edit_profile(request, id):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    User1 = User.objects.get(id=id)
    context = {
        "User1": User1
    }
    return render(request, 'edit.html', context)


def update_profile(request, id):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    errors = User.objects2.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/profile/{id}/edit')

    User1 = User.objects.get(id=id)

    User1.first_name = request.POST['fname'],
    User1.last_name = request.POST['lname'],
    User1.email = request.POST['email']
    User1.save()

    return redirect('/quotes')


def delete_quote(request, id):
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect("/")

    deleted_quote = Quote.objects.get(id=id)
    deleted_quote.delete()
    return redirect('/quotes')
