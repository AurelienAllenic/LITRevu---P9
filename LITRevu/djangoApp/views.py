from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from .models import Ticket
from .models import UserFollows
from .models import Review
from itertools import chain
from .forms import TicketForm, ReviewForm
from operator import attrgetter
import logging

logger = logging.getLogger(__name__)


def home_view(request):
    return render(request, 'home.html')


@login_required(login_url='/')
def flux_view(request):
    displayed_items = set()
    tickets = Ticket.objects.prefetch_related('reviews').all()
    reviews = Review.objects.all()
    combined_list = []
    # Ajoutez les tickets pas encore affichés à la liste combinée
    for ticket in tickets:
        if ticket.id not in displayed_items:
            combined_list.append(ticket)
            displayed_items.add(ticket.id)

    # Ajoutez les critiques pas encore affichées à la liste combinée
    for review in reviews:
        if review.id not in displayed_items:
            combined_list.append(review)
            displayed_items.add(review.id)

    # Trier la liste combinée par time_created
    combined_list = sorted(
                        combined_list,
                        key=attrgetter('time_created'),
                        reverse=True
                        )

    context = {
        'items': combined_list,
    }
    return render(request, 'flux.html', context)


@login_required(login_url='/login/')
def posts_view(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    # Combiner les tickets et les critiques en une seule liste
    combined_items = list(chain(user_tickets, user_reviews))

    # Trier la liste combinée par 'time_created' en ordre décroissant
    combined_items_sorted = sorted(
                                combined_items,
                                key=lambda x: x.time_created,
                                reverse=True
                            )

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
        'rating_range': range(1, 6),
    }
    return render(request, 'createCritic.html', context)


@login_required
def createCriticInResponse_view(request, ticket_id):
    # Récupérer le ticket en fonction de son ID
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST':
        # ReviewForm avec form datas
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Sauvegarder la critique associée au ticket
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flux')
    else:
        # Créer une instance vide de ReviewForm
        review_form = ReviewForm()

    context = {
        'ticket': ticket,
        'review_form': review_form,
    }
    return render(request, 'createCriticInResponse.html', context)


@login_required
def createTicket_view(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        ticket_form = TicketForm()

    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'createTicket.html', context)


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
            if (user_to_follow != request.user and
                not UserFollows.objects.filter(
                    user=request.user, followed_user=user_to_follow
                    ).exists()):
                UserFollows.objects.create(
                                            user=request.user,
                                            followed_user=user_to_follow
                                            )
                messages.success(
                                    request,
                                    f"Vous suivez {username_to_follow}"
                                )
            else:
                messages.error(
                                request,
                                "Vous ne pouvez pas suivre cet utilisateur"
                                )
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
            messages.error(
                            request,
                            'Nom d’utilisateur ou mot de passe incorrect.'
                            )
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
                user = User.objects.create_user(
                                                username=email,
                                                email=email,
                                                password=password1
                                                )
                user.save()
                login(request, user)
                return redirect('home')
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
        reviews = item.reviews.all()
        return render(
                        request,
                        'edit.html',
                        {'item': item, 'reviews': reviews, 'type': 'ticket'}
                    )
    elif type == 'review':
        item = get_object_or_404(Review, pk=id, user=request.user)
        ticket = item.ticket
        print(ticket)
        return render(
                    request,
                    'edit.html',
                    {'item': item, 'ticket': ticket, 'type': 'review'}
                    )
    else:
        return HttpResponseBadRequest('Type non reconnu')


@login_required
def edit_review(request, id):
    try:
        review = Review.objects.get(id=id, user=request.user)
    except Review.DoesNotExist:
        # pas de critique ou pas à l'user
        return redirect('flux')

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('flux')
    else:
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
            return redirect('flux')
    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
        'item': ticket
    }
    return render(request, 'edit.html', context)


@login_required
def delete_post(request, type, id):
    if type == 'ticket':
        ticket = get_object_or_404(Ticket, id=id, user=request.user)
        if ticket.image:
            ticket.image.delete(save=False)
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
            messages.error(
                            request,
                            "Aucun utilisateur n'a été trouvé avec ce nom."
                        )
        user_follows = UserFollows.objects.filter(user=request.user)
        user_followers = UserFollows.objects.filter(followed_user=request.user)
    return render(
                request,
                'subscribes.html',
                {
                    'users': users,
                    'user_follows': user_follows,
                    'user_followers': user_followers
                }
                )


@login_required
def follow_user(request):
    if request.method == 'POST':
        username_to_follow = request.POST.get('username')
        try:
            to_follow = User.objects.get(username=username_to_follow)
            if to_follow != request.user and not UserFollows.objects.filter(
                user=request.user,
                followed_user=to_follow
            ).exists():
                UserFollows.objects.create(
                                            user=request.user,
                                            followed_user=to_follow
                                            )
                messages.success(
                                    request,
                                    f"Vous suivez maintenant"
                                    f"{username_to_follow}"
                                )
            else:
                messages.error(
                                request,
                                "Vous ne pouvez pas suivre cet utilisateur"
                            )
        except User.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé")

    # Actualiser la liste d'abonnements
    user_follows = UserFollows.objects.filter(user=request.user)
    user_followers = UserFollows.objects.filter(followed_user=request.user)

    # Rediriger vers la page précédente après la requête POST
    return render(
                    request,
                    'subscribes.html',
                    {
                        'user_follows': user_follows,
                        'user_followers': user_followers
                    }
                )


@login_required
def unfollow_user(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        try:
            user_to_unfollow = User.objects.get(username=u)
            follow_relation = UserFollows.objects.filter(
                user=request.user,
                followed_user=user_to_unfollow
            ).first()
            if follow_relation:
                follow_relation.delete()
                messages.success(request, f"Vous avez arrêté de suivre {u}")
            else:
                messages.error(request, "Vous ne suivez pas cet utilisateur")
        except User.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé")

    # Rediriger vers la page précédente après la requête POST
    return redirect('subscribes')
