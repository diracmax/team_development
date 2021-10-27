# population_first_app.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

import sys
import random
from accounts.models import CustomUser
from accounts.tests.factories import UserFactory, SampleFollowFactory
from timeline.models import Category, Post
from timeline.tests.factories import SamplePostFactory, SampleApplyFactory, SampleLikeFactory


class UserPopulate():
  display = "アカウント"
  def ready():
    return
  def generate():
    user = UserFactory()
    print("    ユーザー番号: "+str(user.pk)+", \""+user.username+"\"を生成しました")
    return

class PostPopulate():
  display = "投稿"
  def ready():
    if not(CustomUser.objects.all()):
      print("アカウントが存在しないため投稿を作成できません。")
      Populate(model="user", N=1)
    return
  def generate():
    post = SamplePostFactory()
    print("    投稿番号: "+str(post.pk)+", \""+post.title+"\"が生成されました")
    return

class FollowPopulate():
  display = "フォロー"
  def ready():
    if not(CustomUser.objects.all()):
      print("アカウントが2つ以上存在しないため投稿を作成できません。")
      Populate(model="user", N=2)
    return
  def generate():
    follow = SampleFollowFactory()
    print("    フォロー: "+str(follow.follower)+"->"+str(follow.following)+"を生成しました")
    return
    
class ApplyPopulate():
  display = "応募"
  def ready():
    if not(Post.objects.all()):
      print("投稿が存在しません。")
      Populate(model="post", N=1)
    return
  def generate():
    record = SampleApplyFactory()
    print("    応募: "+str(record.user.username)+"->"+str(record.post.title)+"を生成しました")
    return
    
class LikePopulate():
  display = "いいね"
  def ready():
    if not(Post.objects.all()):
      print("投稿が存在しません。")
      Populate(model="post", N=1)
    return
  def generate():
    record = SampleLikeFactory()
    print("    いいね: "+str(record.user.username)+"->"+str(record.post.title)+"を生成しました")
    return


class Populate():
  def __init__(self, model, N):
    self.N=N
    if model == "user":
      model = UserPopulate
    if model == "post":
      model = PostPopulate
    if model == "follow":
      model = FollowPopulate
    if model == "apply":
      model = ApplyPopulate
    if model == "like":
      model = LikePopulate
    self.display = model.display
    self.ready = model.ready
    self.generate = model.generate

  def execute(self):
    self.ready()
    rest = self.N
    count = 0
    flag =False
    while rest:
      try: 
        self.generate()
        rest -= 1
        count = 0
      except django.db.utils.IntegrityError:
        print("    失敗しました")
        count+=1
        if count == 5:
          print("    "+str(count)+"回連続で失敗したので中断します")
          flag = True
          break
    print(str(self.N-rest)+'個の'+self.display+'を作成しました')


def main():
  if len(sys.argv) != 3:
    print("USAGE: make populate user/post/follow/apply/like [N]")
    sys.exit(1)

  N = 1 if len(sys.argv)==2 else int(sys.argv[2])
  model = sys.argv[1]
  populate = Populate(model=model, N=N)
  populate.execute()
  

if __name__ == "__main__":
  main()
