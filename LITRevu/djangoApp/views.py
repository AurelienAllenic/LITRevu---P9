from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Ticket
from django.contrib.auth.decorators import login_required
from .models import UserFollows
from .forms import TicketForm, ReviewForm
from .models import Review
from itertools import chain
from operator import attrgetter
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect
# Assurez-vous d'importer la fonction reverse
from django.urls import reverse
import logging
import json

logger = logging.getLogger(__name__)

def home_view(request):
    # Vue pour la page d'accueil
    return render(request, 'home.html')

def signup_view(request):
    # Vue pour la page des catégories
    return render(request, 'signup.html')

@login_required(login_url='/')
def flux_view(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()

    # Combine tickets et reviews en une seule liste
    combined_list = sorted(
        chain(tickets, reviews),
        key=attrgetter('time_created'),  # Tri par 'time_created'
        reverse=True  # Du plus récent au plus ancien
    )

    context = {
        'items': combined_list,  # Passez la liste combinée sous le nom 'items' au template
    }
    return render(request, 'flux.html', context)


@login_required(login_url='/login/')
def posts_view(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    # Combiner les tickets et les critiques en une seule liste
    combined_items = list(chain(user_tickets, user_reviews))

    # Trier la liste combinée par 'time_created' en ordre décroissant
    combined_items_sorted = sorted(combined_items, key=lambda x: x.time_created, reverse=True)

    context = {
        'items': combined_items_sorted,
    }

    return render(request, 'posts.html', context)

@login_required
def createCritic_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST, request.FILES)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            return redirect('flux')  # Redirige vers la page de votre choix
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form,
        'rating_range': range(1, 6),  # Ajoutez ceci pour passer la plage de notes
    }
    return render(request, 'createCritic.html', context)

@login_required
def createTicket_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')  # Redirigez vers la page de votre choix après la soumission
    else:
        ticket_form = TicketForm()

    context = {
        'ticket_form': ticket_form,  # Passez uniquement ticket_form au contexte
    }
    return render(request, 'createTicket.html', context)  # Assurez-vous d'utiliser le bon template


@login_required(login_url='/')
def list_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'reviews_list.html', {'reviews': reviews})


@login_required(login_url='/')
def subscribes_view(request):
    # Récupérer les utilisateurs que l'utilisateur actuel suit
    user_follows = UserFollows.objects.filter(user=request.user)

    # Récupérer les utilisateurs qui suivent l'utilisateur actuel
    user_followers = UserFollows.objects.filter(followed_user=request.user)

    # Traiter le formulaire pour suivre un nouvel utilisateur
    if request.method == 'POST':
        username_to_follow = request.POST.get('username')
        try:
            user_to_follow = User.objects.get(username=username_to_follow)
            if user_to_follow != request.user and not UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                messages.success(request, f"Vous suivez maintenant {username_to_follow}")
            else:
                messages.error(request, "Vous ne pouvez pas suivre cet utilisateur")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé")

    # Passer les abonnements et les abonnés au template
    return render(request, 'subscribes.html', {
        'user_follows': user_follows,
        'user_followers': user_followers
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('flux')
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
            return redirect('home')
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, "L'adresse email est déjà utilisée.")
            else:
                user = User.objects.create_user(username=email, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('home')  # Redirigez vers la page d'accueil après l'inscription réussie
        else:
            messages.error(request, "Les mots de passe ne correspondent pas.")

    return render(request, 'signup.html')

def tickets_view(request):
    tickets = Ticket.objects.all()  # Récupère tous les tickets
    return render(request, 'tickets.html', {'tickets': tickets})

@login_required
def edit_post(request, type, id):
    
    if type == 'ticket':
        print(type)
        item = get_object_or_404(Ticket, pk=id, user=request.user)
        print(json.dumps(item))
        return render(request, 'edit.html', {'item': item})
    elif type == 'review':
        print(type)
        item = get_object_or_404(Review, pk=id, user=request.user)
        return render(request, 'edit.html', {'item': item})
    else:
        return HttpResponseBadRequest('Type non reconnu')


@login_required
def delete_post(request, type, id):
    if type == 'ticket':
        ticket = get_object_or_404(Ticket, id=id, user=request.user)
        ticket.delete()
        return redirect('posts')
    elif type == 'review':
        review = get_object_or_404(Review, id=id, user=request.user)
        review.delete()
        return redirect('posts')
    else:
        return HttpResponseBadRequest('Type non reconnu')
