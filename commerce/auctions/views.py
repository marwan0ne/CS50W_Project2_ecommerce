
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,  login,  logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import  render
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db import IntegrityError
from django.db.models import F
from .models import *



# A Form for Creating a new item in the auctions.
class CreateForm(forms.Form):
    cateogory_choices =[
        ('other', 'Other'), 
        ('watch', 'watch'), 
        ('cosmatics', 'cosmatics'), 
        ('electronics', 'Electronics'), 
        ('clothe', 'Clothe'), 
        ('sneakers', 'Sneakers'), 
        ('sport-gadget', 'Sport-Gadget'), 
        ('book', 'Book'), 
        ('painting', 'Painting'), 
        ('jewelry', 'jewelry')
    ]
    title = forms.CharField(label='', 
     widget=forms.TextInput(attrs={
        "placeholder":"Enter title", 
        "autocomplete":"off", "class":"form"}))
    image = forms.CharField(label='', required= False, 
         widget=forms.TextInput(attrs={
        "placeholder":"Place place the image url here", 
        "autocomplete":"off", "class":"form"}))
    price = forms.CharField(label='', 
     widget=forms.TextInput(attrs={
        "placeholder":"Enter Price", 
        "autocomplete":"off", "class":"form"}))
    description = forms.CharField(label='', required=False, 
     widget=forms.Textarea(attrs={
        "placeholder":"Enter description", 
        "autocomplete":"off", "class":"form"}))
    category = forms.CharField(label="", required= False, 
      widget = forms.Select(choices=cateogory_choices , attrs={
         
      }))
# A Form for the biding.
class PriceForm(forms.Form):
        biding_price = forms.CharField(label='', 
        widget=forms.TextInput(attrs={
            "placeholder":"Enter your bid.", 
            "autocomplete":"off"}))
class commentForm(forms.Form):
    comment = forms.CharField(label='', 
        widget=forms.TextInput(attrs={
            "placeholder":"Comment", "autocomplete":"off", 
            "class":"comment"
        }
        ))

def index(request):
    # Retriving all the items from the database.
    active = Listing.objects.all()
    # Checking if the user is logged in
    # So we can count the number of items on his watchlist.
    if request.user.is_authenticated:
        # This query for the number of watched item by the user.
        watchers = watchlist.objects.filter(user = request.user, watched=True).count()
        return render(request,  "auctions/index.html", {'lists':active, 'watchers':watchers})
    else:
        return render(request,  "auctions/index.html", {'lists':active})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,  username=username,  password=password)

        # Check if authentication successful
        if user is not None: 
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request,  "auctions/login.html",  {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request,  "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request,  "auctions/register.html",  {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username,  email,  password)
            user.save()
        except IntegrityError:
            return render(request,  "auctions/register.html",  {
                "message": "Username already taken."
            })
        login(request,  user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request,  "auctions/register.html")
def createListing(request):
    # If the method is get then I will show the creation form.
    if request.method == "GET":
        watchers = watchlist.objects.filter(user = request.user, watched=True).count()
        return render(request,  "auctions/create.html", {'watchers':watchers, 
                         'form':CreateForm()
                 })
   # Otherwise it means the user have submited the form.
   # So I will check if it's valid or not.
   # Then I will add it to the database.
    form = CreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid:
            title = request.POST['title']
            image = request.POST['image']
            price =request.POST['price']
            description = request.POST['description']
            category = request.POST['category']
            entry = Listing(title = title,  description = description,  category = category,  
                price = float(price),  image = image,  active = True, creator = request.user)
            entry.save()
            bid = Bid(user = request.user,  item = entry)
            bid.save()
           
            
            return HttpResponseRedirect(reverse("auctions:index"))
def visit(request,  id):
    if request.method == "GET":
        # Checking if the user is loged in or not...
        # To retrive the number of watched item if he is loged in. 
        # Otherwise I will not excute this query.
        if request.user.is_authenticated:
            detail = details(request,id,False,False,True)
        else:
            detail = details(request,id,False,False,False)

        return render(request, "auctions/entry.html", detail)
def deactivate(request, id):
    if request.method == "POST":
        # Changing the object status into unactive
        Listing.objects.filter(id = id).update(active = False)
        return HttpResponseRedirect(reverse("auctions:index"))
def categories(request):
    if request.method == "GET":
        # Counting the number of the watched element
        watchers = watchlist.objects.filter(user = request.user, watched=True).count()
        # Creating a dictionary which contains all the categories.
        infos= {"infos":["watch", "painting", "book", "clothe", "sneakers", "electronics", "cosmatics", "jewelry", 
            "sport-gadget", "other"], "watchers":watchers}
        return render(request, "auctions/category.html", infos)
def category_list(request, category):
    if request.method == "GET":
        # Retriving all the element in this category
        categoriesList = Listing.objects.filter(category = category)
        categorynumber = Listing.objects.filter(category = category).count()
        watchers = watchlist.objects.filter(user = request.user, watched=True).count()
        return render(request, "auctions/categories.html", {'lists':categoriesList, 
        'watchers':watchers,'category':category,
        'categorynumber':categorynumber})
            
        

@login_required
def comment(request, id):
    form = commentForm(request.POST or None)
    if request.method == "POST" and form.is_valid:
        # Taking the submitied comment from the user.
        com = request.POST["comment"]
        # Adding the comment to the comment table saving the user,  the item and th comment.
        save = Comment(user = request.user,  item_id = id,  comment = com)
        save.save()
    # Then I redriect to the visit page.
    return HttpResponseRedirect(reverse("auctions:visit", kwargs={'id':id}))
@login_required
def adding_to_watchlist(request, id):
    if request.method =="POST":
        set = watchlist.objects.filter(user = request.user, item_id = id).values()
        # Checking whtether the item the user intereacted with it before.
        if set.exists():
           # number  = watchlist.objects.filter(user = request.user, item_id = id).count().
           # here I just reverse it's status.
            if set[0]['watched']:
                watchlist.objects.filter(user = request.user, item_id = id).update(watched = False)
            else: 
        
                watchlist.objects.filter(user = request.user, item_id = id).update(watched = True)
        # if it was never on the watchlist then the I will add it and make it assigned as watched
        else:
            watch = watchlist(user =request.user,  item_id = id,  watched = True)
            watch.save()
        return HttpResponseRedirect(reverse("auctions:visit", kwargs={'id':id}))
@login_required
def biding(request,  id):
    form = PriceForm(request.POST or None)
    detail = {}
    if request.method == "POST" and form.is_valid:
        new_price = request.POST["biding_price"]
        listing = Listing.objects.get(id = id)
        
        old_price =listing.price
        if float(new_price) > old_price:
            Listing.objects.filter(id = id).update(price = new_price)
            bider = Bid.objects.filter(user = request.user,item_id = id).values()
            if bider.exists():
                    Bid.objects.filter(user = request.user,item_id = id).update(bid=new_price)
                    Bid.objects.filter(user = request.user,item_id = id).update(numberofbids = F('numberofbids')+1)
            else:
                 newbider = Bid(user = request.user,  item_id = id,bid = new_price,numberofbids =1)
                 newbider.save()
            detail = details(request,id,False,True,True)
       
        else:
           detail = details(request,id,True,False,True)
    return render(request, "auctions/entry.html", detail)
@login_required
def Watchlist(request):
    # if the user want to see his watchlist
    # Then his data will be retrived from the data base and shown to him.
    if request.method == "GET":
        watchers = watchlist.objects.filter(user = request.user, watched=True)
        numberofwatcehr = watchlist.objects.filter(user = request.user, watched=True).count()
        return render(request, "auctions/Watchlist.html", {
            "Watched":watchers, "watchers":numberofwatcehr
        })
# This function consisit of set of queries that are repeated but small changes.
# So to reduce redundancy.
def details(request,id,less,more,logedin):
    comments = Comment.objects.filter(item_id = id)
    bid =  Bid.objects.latest()
    list = Listing.objects.get(id=id)
    Allofbids = Bid.objects.filter(item_id = id)
    # This line calculate the total number of bids occured on an item.
    numberofbids = sum([item.numberofbids for item in Allofbids])
    details = {}
    if logedin:
        watchers = watchlist.objects.filter(user = request.user, watched=True).count()
        
        details = {'list':list, 'watchers':watchers, 'numberofbids':numberofbids,
                    'form':PriceForm(), 'comment':commentForm(), 'bid':bid, 
                    'comments':comments, 'less':less, 'more':more}
    else:
        details = {'list':list, 'numberofbids':numberofbids,
                    'form':PriceForm(), 'comment':commentForm(), 'bid':bid, 
                    'comments':comments, 'less':less, 'more':more}
   
    return details