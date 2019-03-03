from django.db import models
import bcrypt
import re
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.


class UserManager(BaseUserManager):
    def validate(self, form):
        errors = []
        if len(form['first_name']) < 2:
            errors.append("First name must be at least 2 characters long.")

        if len(form['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long.")

        if len(form['password']) < 8 & len(form['confirm_password']) < 8:
            errors.append("Password must be at least 8 characters long.")

        if not EMAIL_REGEX.match(form['email']):
            errors.append("Must be a valid email address.")

        if form['password'] != form['confirm_password']:
            errors.append("You need to confirm the password!")

        existing_email = User.objects.filter(email=form['email'])
        if existing_email:
            errors.append("Email already in use!")
            print(existing_email)

        return errors

    def easy_create(self, form):
        hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        
        if len(User.objects.filter(is_admin=True)) == 0:            
            first_user = User.objects.create(
                first_name=form['first_name'],
                last_name=form['last_name'],
                email=form['email'],
                pw_hash=hashed_pw,
                is_admin=True,
                id=1
            )
            return first_user.id
        else:
            user = User.objects.create(
                first_name=form['first_name'],
                last_name=form['last_name'],
                email=form['email'],
                pw_hash=hashed_pw
            )

            return user.id


    def login(self, form):
        existing_user = User.objects.filter(email=form['email'])

        if existing_user:
            user = existing_user[0]
            if bcrypt.checkpw(form['password'].encode(), user.pw_hash.encode()):
                return(True, user.id)
        return(False, "Email or password incorrect!")


    def edit_personal_info(self, form, user_id):
        user = User.objects.get(id=user_id)
        print(user)
        # user_lev =form['user_level']
        if 'user_level' in form: 
            if form['user_level'] == 'admin':
                user.is_admin = True
                
            elif form['user_level'] == 'normal':
                user.is_admin = False
                
        user.first_name = form['first_name']
        user.last_name = form['last_name']
        user.email = form['email']
        user.save()
        return user


    def edit_passwords(self, form, user_id):
        user = User.objects.get(id=user_id)
        
        if form['password'] == form['confirm_password']:
            pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
            print(pw)
            user.pw_hash = pw
            user.save()
            return user
                           

    def edit_description(self, form, user_id):
        user = User.objects.get(id=user_id)

        user.description = form['description']
        user.save()
        return user
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)

    is_admin = models.BooleanField(default=False, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    objects = UserManager()

    def __repr__(self):
        return "<User: %s>" % self.first_name

    def __str__(self):
        return "<User: %s>" % self.first_name


class MessageManager(models.Manager):
    def create_message(self, form, user_id):
        message = Message.objects.create(
            message = form['message'],
            user = User.objects.get(id=user_id)
        )

        return message.id

class CommentManager(models.Manager):
    def create_comment(self, form, user_id, message_id):
        user = User.objects.get(id=user_id)
        message = Message.objects.get(id=message_id)
        comment = Comment.objects.create(
            comment = form['comment'],
            user = user,
            message = message
        )
        return comment.id



class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

    def __repr__(self):
        return "<Message: %s>" % self.message

    def __str__(self):
        return "<Message: %s>" % self.message


class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="comments")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()

    def __repr__(self):
        return "<Comment: %s>" % self.comment

    def __str__(self):
        return "<Comment: %s>" % self.comment