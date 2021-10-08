from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse,Http404
from .models import Posts

from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate,login
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
API_KEY = settings.API_KEY
import requests
from django.core import serializers

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated 


from django.conf import settings
from .serializers import PostSerializer, PostActionSerializer,PostCreateSerializer
from .forms import PostForm
# Create your views here.

def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login/")
    return render(request,'pages/dashboard.html')


def loginUser(request):
    if request.method=="POST":
        #check the credentials
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request,username=username, password=password)
        print(user)
        print(request.user)
      
        if user is not None:
        # A backend authenticated the credentials
            login(request, user)
            return redirect("/home/")
        else:
        # No backend authenticated the credentials

            return redirect("/login/")

    return render(request,'pages/login.html')

def registerUser(request):
    if request.method =="POST":
        #first_name = request.POST['first_name']
        #last_name = request.POST['last_name']
        username = request.POST['username']
        pass1 = request.POST['password']
        pass2 = request.POST['password_confirm']
        email = request.POST['email']
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                print('username taken')
            else:
                user = User.objects.create_user(username=username, password=pass1, email=email)
                user.save()
                print("user created")
            print("not")
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request,'pages/register.html',{'form':form})


def logoutUser(request):
    logout(request)
    return redirect(("/login/"))



def dashboard(request, *args, **kwargs):
    if request.user.is_anonymous:
        return redirect("/login/")
    print(request.user or None)
    print("home",request.user or None)
    qs = Posts.objects.filter(user=request.user)
    #qs = serializers.serialize("json",Posts.objects.filter(user=request.user))

    if request.method=="POST":
        #a = request.method
        try:
            if request.POST['opt']=="delete":
                id =  request.POST['p_id']
                Posts.objects.filter(id=id).delete()
                return render(request,"pages/dashboard.html",context={'qs':qs},status=200)
        except:
            new_content = request.POST['content']
            title = request.POST['title']
            new_post = Posts(user=request.user,content=new_content,title=title)
            new_post.save()
    

    print(qs)
    return render(request,"pages/dashboard.html",context={'qs':qs},status=200)

def newsFeed(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    url = f'https://newsapi.org/v2/everything?q=Apple&from=2021-10-06&sortBy=popularity&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles':articles
    }

    return render(request,'pages/home.html',context)


@api_view(['POST']) #http method the client ==POST
#@authentication_classes([SessionAuthentication,MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
def post_create_view(request,*args, **kwargs):
    print("pcr")
    serializer = PostCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def post_detail_view(request,post_id,*args,**kwargs):
    print("pdv")
    qs = Posts.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)

    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(["GET", 'DELETE', 'POST'])
@permission_classes([IsAuthenticated]) # REST API course
def post_delete_view(request,post_id,*args,**kwargs):
    qs = Posts.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You can not delete this post"}, status=401)
    obj = qs.first()
    obj.delete()
    #serializer = PostSerializer(obj)
    return Response({"message":"Post removed"}, status=200)




@api_view(['GET'])
def post_list_view(request,*args,**kwargs):
    qs = Posts.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)


