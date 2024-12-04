from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import re
from decimal import Decimal


from .forms import CommentForm, BidForm, SearchForm, AuctionListingForm
from .models import AuctionListing, Bid, Comment, User


def index(request):
    auctionslist = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {'lists':auctionslist})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "/Users/aryanabsalan/Desktop/commerce/auctions/templates/auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "/Users/aryanabsalan/Desktop/commerce/auctions/templates/auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "/Users/aryanabsalan/Desktop/commerce/auctions/templates/auctions/register.html")


def listing(request, p_id):
    current = get_object_or_404(AuctionListing, pk=p_id)
    bid = Bid.objects.filter(auction=current).order_by('amount').last()
    comments = Comment.objects.filter(auction=current).order_by('-id')
    return render(request, 'auctions/comments.html', {
        'auction': current,
        'bid':bid,
        'bid_form':BidForm(),
        'comments': comments,
        'comment_form':CommentForm(),
        'user': request.user,
    })

def add_comment(request, p_id):
    requser = str(request.user)
    if request.user.is_authenticated :
        form = CommentForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            print(form)
            comment = Comment(user = request.user, auction = get_object_or_404(AuctionListing, id=p_id), **form)
            comment.save()

            return HttpResponseRedirect(reverse('listing', kwargs={'p_id':p_id}))

    else:
        return render(request, 'auctions/login.html', {'message': 'Must be logged in to be able to comment!'})


def add_bid(request, p_id):
    requser = str(request.user)
    if request.user.is_authenticated :
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_form = bid_form.cleaned_data
            bid_form = str(bid_form)
            print(bid_form ,type(bid_form))

            
            match = re.search(r"Decimal\('([\d\.]+)'\)", bid_form)
            number = Decimal(match.group(1))
            print(number)

            bid = Bid(user = request.user, auction = get_object_or_404(AuctionListing, id=p_id),amount = number)
            bid.save()

            return HttpResponseRedirect(reverse('listing', kwargs={'p_id':p_id}))

    else:
        return render(request, 'auctions/login.html', {'message': 'Must be logged in to be able to Add Bid!'})



def search_items(request):
    q = request.GET.get("search_items").lower()
    return render(request, 'auctions/search_results.html', {
        'results': AuctionListing.objects.filter(category=q)
    })



def category(request):
    category = AuctionListing.objects.all()
    
    return render(request, 'auctions/category.html', {'list' : category})



@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


@login_required
def watch(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    request.user.watchlist.add(auction)
    request.user.watchlist_counter += 1
    request.user.save()
    return HttpResponseRedirect(reverse('index'))


@login_required
def unwatch(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    request.user.watchlist.remove(auction)
    request.user.watchlist_counter -= 1
    request.user.save()
    if '/unwatch/' in request.path:
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('watchlist'))


@login_required(login_url='auctions/login.html')
def create(request):
    return render(request, "auctions/create.html", {
        'form': AuctionListingForm()
    })


@login_required(login_url='auctions/login.html')
def insert(request):
    form = AuctionListingForm(request.POST)
    if form.is_valid():
        auction = AuctionListing(user=request.user, **form.cleaned_data)
        if not auction.image_url:
            auction.image_url = 'https://pineridge.glfconnect.com/store/content/images/thumbs/default-image_450.png'
        auction.save()
        start_bid = auction.start_bid
        bid = Bid(amount=start_bid, user=request.user, auction=auction)
        bid.save()
        print("auction:" + auction.image_url)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/create.html', {
            'form': form,
            'error': form.errors
        })

@login_required(login_url='auctions/login.html')
def close_bid(request, p_id):
    auction = get_object_or_404(AuctionListing, id=p_id)
    auction.price = 0
    auction.save()
    print("auction closed")

    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='auctions/login.html')
def del_bid(request, p_id):
    auction = get_object_or_404(AuctionListing, id=p_id)
    auction.delete()

    return HttpResponseRedirect(reverse('index'))