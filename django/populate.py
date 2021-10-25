# population_first_app.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import sys
import random
from accounts.models import CustomUser
from accounts.tests.factories import UserFactory
from timeline.models import Category, Post
from timeline.tests.factories import SamplePostFactory


def user_populate(N=5):
  print('アカウントを自動生成しています...')
  c = 0
  for entry in range(N):
    # post = PostFactory(category_exist=True)
    try: 
      user = UserFactory()
      print("    ユーザー番号: "+str(user.pk)+", \""+user.username+"\"が生成されました")
    except django.db.utils.IntegrityError:
      print("    user"+str(entry)+"は既に存在します")
      c += 1
  print(str(N-c)+'個のアカウントを作成しました')

def post_populate(N=5):
  if not(CustomUser.objects.all()):
    print("アカウントが存在しないため投稿を作成できません。")
    user_populate(1)
  print('投稿を自動生成しています...')
  for entry in range(N):
    # post = PostFactory(category_exist=True)
    post = SamplePostFactory()
    print("    投稿番号: "+str(post.pk)+", \""+post.title+"\"が生成されました")
  print(str(N)+'個の投稿を作成しました')


def main():
  if len(sys.argv) != 3:
    print(sys.argv)
    print("USAGE: make populate user/post [N]")
    sys.exit(1)

  N = 5 if len(sys.argv)==2 else int(sys.argv[2])

  if sys.argv[1] == "user":
    user_populate(N)
  if sys.argv[1] == "post":
    post_populate(N)
  

if __name__ == "__main__":
  main()
