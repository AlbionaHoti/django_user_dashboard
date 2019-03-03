from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
from django.core.urlresolvers import reverse

# Create your views here.


def index(request):
    if 'user_id' not in request.session:
        return render(request, 'main/index.html')

    return redirect('users:dashboard')


def create(request):
    print(request.POST)

    errors = User.objects.validate(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)

        return redirect('users:index')

    user_id = User.objects.easy_create(request.POST)
    request.session['user_id'] = user_id
    
    print('SESSION USER ID: ', request.session['user_id'])
    return redirect('users:dashboard')

def create_user(request):
    print("REQUEST POST: ",request.POST['first_name'])

    errors = User.objects.validate(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)

        return redirect('users:index')

    user_id = User.objects.easy_create(request.POST)
    print("NEW USER: ", user_id)
    return redirect('users:dashboard')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('users:index')

    is_user = request.session['user_id']

    if len(User.objects.filter(is_admin=True)) == 1:
        # is_admin = User.objects.get(is_admin=True)
        is_admin = User.objects.first()

    
        if is_user == is_admin.id:
            request.session['admin_id'] = is_admin.id
    elif len(User.objects.filter(is_admin=True)) > 1:
        pass

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "users": User.objects.all()
    }

    return render(request, 'main/dashboard.html', context)


def logout(request):
    request.session.clear()
    return redirect('users:index')


def login(request):
    valid, result = User.objects.login(request.POST)

    if not valid:
        messages.error(request, result)
        return redirect('users:index')

    request.session['user_id'] = result
    return redirect('users:dashboard')


def signin(request):
    return render(request, 'main/signin.html')


def register(request):
    return render(request, 'main/register.html')


def new(request):
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }

    return render(request, 'main/add_new.html', context)


def remove(request, user_id):
    print("USER ID: -- remove ", user_id)
    # check if is admin
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('users:dashboard')



def edit(request, user_id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "edit_user": User.objects.get(id=user_id)
    }   
    return render(request, 'main/edit_user_info.html', context)



def edit_personal_info(request, user_id):
    print("Update mode: ", user_id)
    updated_user = User.objects.edit_personal_info(request.POST, user_id)
    return redirect(reverse('users:edit', kwargs={"user_id": updated_user.id}))
  
    
def edit_passwords(request, user_id):
    print("Update passwords mode: ", user_id)
    updated_password = User.objects.edit_passwords(request.POST, user_id)
    return redirect(reverse('users:edit', kwargs={"user_id": updated_password.id}))


def edit_description(request, user_id):
    updated_description = User.objects.edit_description(request.POST, user_id)
    return redirect(reverse('users:edit', kwargs={"user_id": updated_description.id}))



def wall(request):
    if 'user_id' not in request.session:
        return redirect('wall:index')

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "messages": Message.objects.order_by("-created_at"),
        "comments": Comment.objects.order_by("-created_at")
    }

    return render(request, 'main/wall.html', context)


def message(request):
    print("Message place:", request.POST['message'])
    user_id = request.session['user_id']
    Message.objects.create_message(request.POST, user_id)
    return redirect('users:wall')


def comment(request, message_id):

    print(request.POST)
    print("MESSAGE ID: ", message_id)
    request.session['message_id'] = message_id
    print("USER ID: ", request.session['user_id'])
    user_id = request.session['user_id']
    Comment.objects.create_comment(request.POST, user_id, message_id)
    
    return redirect('users:wall')
    

def delete_comment(request, comment_id):
    print("COMMENT ID:", comment_id)
    comm = Comment.objects.get(id=comment_id)
    print("COMMENT user ID:", comm.user.id)
    print("REQUEST SESSION USER ID: ", request.session['user_id'])
    admin = request.session['admin_id']
    if comm.user.id == request.session['user_id']:
            
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect(reverse('users:wall'))
    elif admin:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect(reverse('users:wall'))
    else:
        return redirect(reverse('users:wall'))


        return redirect(reverse('users:wall'))
