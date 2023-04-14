import datetime
import json
import requests
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from account.models import Profile
from post.models import Post


UserModel: User = get_user_model()


class Command(BaseCommand):
    help = 'Add fake post & user data.'

    def handle(self, *args, **options):
        users, posts = self.get_data()
        for user in users:
            try:
                self.create_user(user)
            except Exception:
                print('an error occurred in create user!')
        for post in posts:
            try:
                self.create_post(post)
            except Exception:
                print('an error occurred in create post!')

    @staticmethod
    def get_data():
        with open('./fake-users.json') as f:
            users = json.load(f)
        with open('./fake-posts.json') as f:
            posts = json.load(f)
        return users, posts

    @staticmethod
    def create_user(user):
        user_obj = UserModel.objects.create_user(
            user['username'],
            email=user['email'],
            password=user['password'],
            first_name=user['first_name'],
        )
        user_obj.save()
        profile: Profile = user_obj.profile
        response = requests.get(user['photo'])
        profile.photo.save(
            f"{user['username']}.jpg",
            ContentFile(response.content),
            save=False,
        )
        date = datetime.datetime.strptime(
            user['date_of_birth'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        profile.date_of_birth = datetime.datetime.strftime(date, "%Y-%m-%d")
        profile.bio = user["description"][:127]
        profile.save()

    @staticmethod
    def create_post(post):
        date = datetime.datetime.strptime(
            post['created'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        created = datetime.datetime.strftime(date, "%Y-%m-%d")
        creator = UserModel.objects.order_by('?').first()
        post_obj = Post(
            user=creator,
            description=f"{post['description']}\n{post['tag']}",
        )
        post_obj.created = created
        response = requests.get(post['photo'])
        format = response.url.rsplit('.', 1)[-1]
        post_obj.image.save(
            f"{post_obj.slug}.{format}",
            ContentFile(response.content),
            save=False,
        )
        users = UserModel.objects.count()
        like_count = random.randint(0, users)
        users_like = UserModel.objects.order_by("?")[:like_count]
        post_obj.total_likes = like_count
        post_obj.save()
        post_obj.tags.clear()
        post_obj.tags.add(post['tag'])
        post_obj.users_like.add(*users_like)
        post_obj.save()
