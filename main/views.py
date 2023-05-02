from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import CreateUserForm, LogInForm, CreateMessageForm, ChangeProfileForm
from .models import User, Message


def index(request, UserName=''):
    if UserName == '':
        if request.session.get('CurrentUserName') is None:
            return render(request, 'main/auth.html')
        else:
            return redirect(reverse('messages', args=[request.session.get('CurrentUserName')]))
    else:
        return redirect(reverse('messages', args=[UserName]))


def auth(request):
    if request.session.get('CurrentUserName'):
        return redirect(reverse('home'))
    return render(request, 'main/auth.html')


def login(request):
    if request.session.get('CurrentUserName'):
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            request.session['CurrentUserName'] = user.UserName
            return redirect(reverse('home'))
    else:
        form = LogInForm()
    return render(request, 'main/login.html', {'form': form})


def signup(request):
    if request.session.get('CurrentUserName'):
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.Age = User.calculate_age(form.cleaned_data['Birthday'])
            user.save()
            request.session['CurrentUserName'] = user.UserName
            return redirect(reverse('home'))
    else:
        form = CreateUserForm()
    return render(request, 'main/signup.html', {'form': form})


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def friends(request, UserName):
    if request.session.get('CurrentUserName') is None or str(request.session.get('CurrentUserName')) != str(UserName):
        return HttpResponseForbidden("You do not have permission to access this page.")
    user = get_object_or_404(User, UserName=UserName)
    return render(request, 'main/friends.html', {'user': user})


def messages(request, UserName, ChatName=None):
    SearchedChat = request.GET.get('SearchedChat')
    if request.session.get('CurrentUserName') is None or str(request.session.get('CurrentUserName')) != str(UserName):
        return HttpResponseForbidden("You do not have permission to access this page.")
    user = get_object_or_404(User, UserName=UserName)
    messages_ = Message.objects.filter(Sender=user) | Message.objects.filter(Recipient=user)
    chats = set([m.Sender for m in messages_] + [m.Recipient for m in messages_])
    if user in chats:
        chats.remove(user)
    if SearchedChat is not None:
        search_res = set(User.objects.filter(UserName__startswith=SearchedChat))
        if user in search_res:
            search_res.remove(user)
    else:
        search_res = None
    if ChatName is not None:
        if User.objects.filter(UserName=ChatName).exists() and UserName != ChatName:
            chat = get_object_or_404(User, UserName=ChatName)
            user_messages = (Message.objects.filter(Sender=user) & Message.objects.filter(Recipient=chat)) | (
                        Message.objects.filter(Sender=chat) & Message.objects.filter(Recipient=user))
            if request.method == 'POST':
                form = CreateMessageForm(request.POST)
                if form.is_valid():
                    text = request.POST['Text']
                    Message.objects.create(Sender=user, Recipient=chat, Text=text)
                    return redirect(reverse('messages', args=[user.UserName, ChatName]))
                else:
                    print(form.errors)
                    for i in form.errors:
                        print(i)
            else:
                form = CreateMessageForm()
            return render(request, 'main/messages.html', {'user': user, 'current_chat': chat, 'chats': chats, 'messages': user_messages, 'form': form, 'search_res': search_res})
        else:
            return redirect(reverse('messages', args=[user.UserName]))
    else:
        return render(request, 'main/messages.html', {'user': user, 'current_chat': None, 'chats': chats, 'messages': None, 'form': None, 'search_res': search_res})


def profile(request, UserName):
    if request.session.get('CurrentUserName') is None or str(request.session.get('CurrentUserName')) != str(UserName):
        return HttpResponseForbidden("You do not have permission to access this page.")
    user = get_object_or_404(User, UserName=UserName)
    if request.method == 'POST':
        form = ChangeProfileForm(user, request.POST)
        if not form.errors.get('FirstName'):
            user.FirstName = form.cleaned_data['FirstName']
        if not form.errors.get('SecondName'):
            user.SecondName = form.cleaned_data['SecondName']
        if not form.errors.get('UserName'):
            user.UserName = form.cleaned_data['UserName']
        if not form.errors.get('Email'):
            user.Email = form.cleaned_data['Email']
        if not form.errors.get('Birthday'):
            user.Birthday = form.cleaned_data['Birthday']
        if form.cleaned_data.get('CurrentPassword') and not form.errors.get('CurrentPassword') and not form.errors.get('NewPassword') and not form.errors.get('ConfirmPassword'):
            user.Password = form.cleaned_data['NewPassword']
        user.save()
        request.session['CurrentUserName'] = user.UserName
    else:
        form = ChangeProfileForm(user)
    return render(request, 'main/profile.html', {'user': user, 'form': form})

