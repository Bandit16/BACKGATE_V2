
from django.shortcuts import redirect, render
from core.filters import PostFilter
from .forms import MemberForm
from .models import Member , Posts , ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.



def homepage(request):
    users = Member.objects.all()
    usernames = User.objects.values_list('username', flat=True)
    posts = Posts.objects.all().order_by('-date_created')[:2]
    context = {

        'users': users,
        'usernames': usernames,
        'posts':posts
    }

    return render(request, 'core/home.html', context)


def accountSettings(request):
    user = request.user.member
    form = MemberForm(
        initial={'username': request.user.username}, instance=user)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            user = request.user
            user.username = form.cleaned_data['username']
            user.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'core/account_setting.html', context)


def post(request):
    posts = Posts.objects.all().order_by('-date_created')
    f = PostFilter(request.GET , queryset=posts)
    posts = f.qs
    search_value = request.GET.get('description')
    
  
    context={
         'filter': f,
        "posts":posts,
        "search_value":search_value
    }
    if request.user.is_anonymous:
        return render(request, 'core/post.html', context)
    else:
        context = {
        'filter': f,
        "posts":posts,
        "search_value":search_value
        }
    
           
    
        if request.method == 'POST':
            member = request.user.member
            print('member')
            description = request.POST.get('description')
            post_picture = request.FILES.get('post_picture')
            post_video = request.FILES.get('post_video')
            
            new_post = Posts.objects.create(
                member=member,
                description=description,
                post_picture=post_picture,
                post_video=post_video

            )
           

    return render(request, 'core/post.html', context)




def personalposts(request, id):
    member = Member.objects.get(id=id)
    posts = member.posts_set.all().order_by('-date_created')
    f = PostFilter(request.GET, queryset=posts)
    posts = f.qs
    context ={
        'posts':posts,
        'member': member
    }
    
    return render(request,'core/personal_post.html',context)


def post_delete(request,id):
    post = Posts.objects.get(id=id)
    if request.method =='POST':
        post.delete()
        return redirect('/')
    context = {
        'post':post
    }
    return render(request,'core/delete.html',context)
@login_required
def chat(request , room_name):
    print(request.user.member.profile_pic.url)
    data = {
        'room_name': room_name,
        'username' : request.user.username,
        'profile_pic':request.user.member.profile_pic.url
        }
    return render(request,'core/chat.html',data)
@login_required
def room(request):
    return render(request,'core/room.html')

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        sender_username = request.user.username
        room_name = request.POST.get('room_name', 'backgate')  # default value is backgate

        # Retrieve the Member instance
        sender = Member.objects.get(user__username=sender_username)

        chat_message = ChatMessage(file=file, sender=sender, room_name=room_name)
        chat_message.save()
        print(chat_message.file.url)
        return JsonResponse({'url': chat_message.file.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)