from hashlib import blake2b
import secrets
from tkinter import CASCADE
from django.db import models
from django.utils import timezone
from django.contrib.auth import models as m

# Create your models here.
class User(m.User):
    #username = models.CharField(max_length=20, unique=True)
    #password = models.CharField(max_length=150)

    name = models.CharField(max_length=50)
    info = models.CharField(max_length=255)
    date_created = models.DateTimeField('date created')

    # True if {password} is user's password
    def check_password(username, password):
        #Store password as f'blake2b${salt}${hashed_string}'
        user = User.objects.filter(username=username).first()
        _data = user.password.split('$')
        _fn = _data[0]
        _salt = _data[1]
        _hash = _data[2]

        if _fn == 'blake2b':
            password_to_check = User.hash_password(password, _salt).split('$')[2]
            return _hash == password_to_check
        else:
            return False

    # Hash with Blake2b() and salt
    def hash_password(password, salt = None):
        bsalt = salt if salt is not None else secrets.token_hex(8)
        bpass = bytes(str(password), 'UTF-8')
        btb = blake2b(salt=bytes(bsalt, 'UTF-8'))
        btb.update(bpass)
        hashedpass = btb.hexdigest()
        return f'blake2b${bsalt}${hashedpass}'

    def __str__(self):
        return self.username

class Subscription(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

def create_user(username, password, name, info='', date=timezone.now()):
    pw = User.hash_password(password)
    if User.objects.filter(username=username).first():
        return False
    u = User(username=username, password=pw, name=name, info=info, date_created=date)
    u.save()
    return u

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=50, unique=True)
    text = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField('date created')

    def __str__(self):
        return self.name
