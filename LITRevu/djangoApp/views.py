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
        item = get_object_or_404(Ticket, pk=id, user=request.user)
        reviews = item.reviews.all()  # Récupérer toutes les critiques associées à ce ticket
        return render(request, 'edit.html', {'item': item, 'reviews': reviews, 'type': 'ticket'})
    elif type == 'review':
        item = get_object_or_404(Review, pk=id, user=request.user)
        ticket = item.ticket  # Récupérer le ticket associé à cette critique
        print(ticket)
        return render(request, 'edit.html', {'item': item, 'ticket': ticket, 'type': 'review'})
    else:
        return HttpResponseBadRequest('Type non reconnu')



@login_required
def edit_review(request, id):
    # Récupérer la critique à éditer
    try:
        review = Review.objects.get(id=id, user=request.user)
    except Review.DoesNotExist:
        # Gérer le cas où la critique n'existe pas ou n'appartient pas à l'utilisateur
        return redirect('flux')  # Rediriger vers la page de votre choix

    if request.method == 'POST':
        # Traitement du formulaire soumis pour mettre à jour la critique
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('flux')  # Rediriger vers la page de votre choix après la mise à jour
    else:
        # Afficher le formulaire de modification de la critique avec les données existantes pré-remplies
        review_form = ReviewForm(instance=review)

    context = {
        'review_form': review_form,
    }
    return render(request, 'edit_review.html', context)

@login_required
def edit_ticket(request, id):
    # Récupérer le ticket à éditer
    ticket = get_object_or_404(Ticket, pk=id, user=request.user)
    if request.method == 'POST':
        # Créer une instance de TicketForm avec les données de la requête
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('flux')  # Rediriger vers la page de votre choix après la modification
    else:
        # Créer une instance de TicketForm avec l'instance de ticket existante
        form = TicketForm(instance=ticket)

    # Passer le formulaire au contexte du rendu
    context = {
        'form': form,
        'item': ticket
    }
    return render(request, 'edit.html', context)


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

def search_users(request):
    users = []
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        users = User.objects.filter(username__icontains=search_query)
        if not users:
            messages.error(request, "Aucun utilisateur n'a été trouvé avec ce nom.")
    return render(request, 'subscribes.html', {'users': users})

@login_required
def follow_user(request):
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

    # Actualiser la liste d'abonnements
    user_follows = UserFollows.objects.filter(user=request.user)

    # Rediriger vers la page précédente après la requête POST
    return render(request, 'subscribes.html', {'user_follows': user_follows})

@login_required
def unfollow_user(request):
    if request.method == 'POST':
        username_to_unfollow = request.POST.get('username')
        try:
            user_to_unfollow = User.objects.get(username=username_to_unfollow)
            follow_relation = UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).first()
            if follow_relation:
                follow_relation.delete()
                messages.success(request, f"Vous avez arrêté de suivre {username_to_unfollow}")
            else:
                messages.error(request, "Vous ne suivez pas cet utilisateur")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé")

    # Rediriger vers la page précédente après la requête POST
    return redirect('subscribes')