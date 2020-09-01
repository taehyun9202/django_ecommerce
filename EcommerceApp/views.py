from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db.models import Q
import bcrypt

# Create your views here.
def home(request):
    allitem = Item.objects.all()
    if 'loginid' not in request.session:
        context = {
            'user': "guest",
            'items': allitem,
        }
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        context = {
                'user': getuser,
                'items': allitem,
        }
    return render(request, "home.html", context)

def base(request):
    if 'loginid' not in request.session:
        context = {
            'user': "guest"
        }
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        context = {
                'user': getuser
        }
    return render(request, "base.html", context)

def search(request):
    searchtext = request.POST['searchtext']
    request.session['searchtext'] = searchtext
    return redirect('/search/'+searchtext)

def searchedItem(request, searchtext):
    searcheditem = Item.objects.filter((Q(name__contains=request.session['searchtext']) |
                                       Q(category__contains=request.session['searchtext']) |
                                       Q(brand__contains=request.session['searchtext'])))
    if 'loginid' not in request.session:
        context = {
            'user': "guest",
            'items': searcheditem,
        }
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        context = {
                'user': getuser,
                'items': searcheditem,
        }
    return render(request, "search.html", context)

def byCategory(request, bycategory):
    print("***************************")
    print(bycategory)
    items = Item.objects.filter((Q(name__contains=bycategory) |
                                       Q(category__contains=bycategory) |
                                       Q(brand__contains=bycategory)))
    if 'loginid' not in request.session:
        context = {
            'user': "guest",
            'items': items,
        }
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        context = {
                'user': getuser,
                'items': items,
        }
    return render(request, "search.html", context)

def signup(request):
    return render(request, "signup.html")

def register(request):
    errors = User.objects.registerVal(request.POST)
    if len(errors) > 0:
        for keys, val in errors.items():
           messages.error(request, val)
        return redirect('/signup')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        password = pw_hash
    )
    if newuser:
        request.session['loginid'] = newuser.id
    return redirect('/')

def signin(request):
    return render(request, "signin.html")

def login(request):
    errors = User.objects.loginVal(request.POST)
    if len(errors) > 0:
        for keys, val in errors.items():
           messages.error(request, val)
        return redirect('/signin')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['loginid'] = logged_user.id
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect("/")

def item(request, itemid):
    getitem = Item.objects.get(id = itemid)
    otheritem = Item.objects.exclude(id = itemid)
    getoptions = Option.objects.filter(item = getitem)
    if 'loginid' not in request.session:
        context = {
            'user': "guest",
            'item': getitem,
            'options': getoptions,
            'others': otheritem
        }
    else:
        getuser = User.objects.get(id = request.session['loginid'])
        context = {
            'user': getuser,
            'item': getitem,
            'options': getoptions,
            'others': otheritem
        }
    return render(request, 'item.html', context)

def addtoCart(request, itemid):
    getuser = User.objects.get(id = request.session['loginid'])
    getitem = Item.objects.get(id = itemid)
    getoption = Option.objects.get(id = request.POST['selected'])
    total = getitem.price + getoption.extra
    if getoption:
        addtoCart = List.objects.create(
        currentuser = getuser,
        obj = getitem,
        selected = getoption,
        total = total,
        quantity = request.POST['quantity']
        )
    return redirect('/cart')

def cart(request):
    if 'loginid' not in request.session:
        return redirect('/')
    getuser = User.objects.get(id = request.session['loginid'])
    allitemlist = List.objects.filter(currentuser = getuser)
    context = {
        'user': getuser,
        'alllist': allitemlist,
    }
    return render(request, 'cart.html', context)

def contact(request):
    if 'loginid' not in request.session:
        return redirect('/')
    getuser = User.objects.get(id = request.session['loginid'])
    context = {
            'user': getuser
    }
    return render(request, 'contact.html', context)

def sendemail(request):
    # send_mail(sub, msg, from ,to, fail_silently=True) //form
    from_email = request.POST.get('email', '')
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    to_list = [settings.EMAIL_HOST_USER]
    # print('***************')
    # print(from_email)
    # print(type(from_email))
    # print(subject)
    # print(message)
    # print(from_email)
    # print(to_list)
    # print('***************')
    if subject and message and from_email:
        send_mail(
            subject,
            from_email+" "+message,
            from_email,
            to_list,
            fail_silently=False)
    return redirect('/')
