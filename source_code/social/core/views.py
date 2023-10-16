from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, Follow


@login_required(login_url="signin")
def index(request):
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)

  posts = Post.objects.all()
  # user_likes = LikePost.objects.filter(username=request.user.username)
  return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts })

@login_required(login_url="signin")
def upload(request):
  if request.method == "POST":

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user = user_profile
    image = request.FILES.get('image_upload')
    caption = request.POST['caption']

    new_post = Post.objects.create(user=user, image=image, caption=caption)
    new_post.save()

    return redirect('/')
  else:
    return redirect('/')

@login_required(login_url="signin")
def like_post(request):
  user = Profile.objects.get(user=request.user)
  post_id = request.GET.get('post_id')
  post = Post.objects.get(id=post_id)
  

  like_filter = LikePost.objects.filter(post=post, user=user).first()
  if like_filter == None:
    new_like = LikePost.objects.create(post=post, user=user)
    new_like.save()
    post.no_of_likes = post.no_of_likes + 1
    post.save()
    return redirect('/')
  else:
    like_filter.delete()
    post.no_of_likes = post.no_of_likes - 1
    post.save()
    return redirect('/')

def profile(request, pk):
  user_object = User.objects.get(username=pk)
  user_profile = Profile.objects.get(user=user_object)
  user_posts = Post.objects.filter(user=user_profile)
  user_post_length = len(user_posts)

  context = {
    'user_object': user_object,
    'user_profile': user_profile,
    'user_posts': user_posts,
    'user_post_length': user_post_length,
  }

  return render(request, 'profile.html', context)

@login_required(login_url="signin")
def follow(request):
  if request.method == "POST":
    follower = Profile.objects.get(user=request.user)

    followee_user_object = User.objects.get(username=request.POST['followee'])
    followee = Profile.objects.get(user=followee_user_object)
    print(follower)
    print(followee)

    if Follow.objects.filter(follower=follower, followee=followee).first():
      delete_follower = Follow.objects.get(follower=follower, followee=followee)
      delete_follower.delete()
      return redirect('/profile/'+followee_user_object.username)
    else:
      new_follower = Follow.objects.create(follower=follower, followee=followee)
      new_follower.save()
      return redirect('/profile/'+followee_user_object.username)
  else:
    return redirect('/')

@login_required(login_url="signin")
def settings(request):
  user_profile = Profile.objects.get(user=request.user)

  if request.method == "POST":
    if request.FILES.get('image') == None:
      image = user_profile.profile_img
      bio = request.POST['bio']
      location = request.POST['location']

      user_profile.profile_img = image
      user_profile.bio = bio
      user_profile.location = location
      user_profile.save()

    if request.FILES.get('image') != None:
      image = request.FILES.get('image')
      bio = request.POST['bio']
      location = request.POST['location']

      user_profile.profile_img = image
      user_profile.bio = bio
      user_profile.location = location
      user_profile.save()

    return redirect('settings')

  else:
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

  if request.method == "POST":
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2:
      if User.objects.filter(email=email).exists():
        messages.info(request, 'Email already in use')
        return redirect('signup')
      elif User.objects.filter(username=username).exists():
        messages.info(request, 'Username already in use')
        return redirect('signup')
      else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        #Log user in and redirect to settings page
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        #create a Profile object for new user
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('settings')
    else:
      messages.info(request, 'Passwords do not match')
      return redirect('signup')

  else:
    return render(request, 'signup.html')

def signin(request):
  
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
      auth.login(request, user)
      return redirect('/')
    else:
      messages.info(request, 'Invalid credentials')
      return redirect('signin')

  else:
    return render(request, 'signin.html')

@login_required(login_url="signin")
def logout(request):
  auth.logout(request)
  return redirect('signin')