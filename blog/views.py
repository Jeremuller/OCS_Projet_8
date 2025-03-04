from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Review
from . import forms
from authentication.forms import FollowUsersForm
from authentication.models import User
from itertools import chain
from django.db.models import Q


@login_required
def home(request):
    """
    Displays the home page with tickets and reviews of the current user
    and the users they follow. Posts are sorted by creation time (newest first).

    Context:
        posts (list): A combined list of tickets and reviews sorted by their
                      creation time.
    """

    user = request.user

    # Fetch tickets the user or users they follow have created
    viewable_tickets = Ticket.objects.filter(
        Q(user=user) | Q(user__in=user.follows.all())
    ).select_related("image")

    # Fetch reviews written by the user or about tickets of the user or their followed users
    viewable_reviews = Review.objects.filter(
        Q(user=user) | Q(ticket__user=user) | Q(ticket__user__in=user.follows.all())
    ).select_related("ticket__image")

    # Combine tickets and reviews into one list of posts
    tickets = [{"type": "ticket", "ticket": ticket} for ticket in viewable_tickets]

    reviews = [
        {"type": "review", "review": review, "ticket": review.ticket}
        for review in viewable_reviews
    ]

    # Sort the posts by their creation time (most recent first)
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: (
            post["review"].time_created
            if post["type"] == "review"
            else post["ticket"].time_created
        ),
        reverse=True,
    )

    context = {"posts": posts}

    return render(request, "blog/home.html", context)


@login_required
def user_posts(request):
    """
    Displays posts (tickets and reviews) created by the logged-in user.

    Context:
        posts (list): A combined list of tickets and reviews created by the user.
    """

    # Fetch the user's tickets and reviews
    user_tickets = request.user.ticket_set.all().select_related("image")

    user_reviews = request.user.review_set.select_related("ticket__image")

    # Combine the tickets and reviews into a list of posts
    tickets = [{"type": "ticket", "ticket": ticket} for ticket in user_tickets]
    reviews = [
        {"type": "review", "review": review, "ticket": review.ticket}
        for review in user_reviews
    ]

    # Sort the posts by their creation time (most recent first)
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: (
            post["review"].time_created
            if post["type"] == "review"
            else post["ticket"].time_created
        ),
        reverse=True,
    )

    context = {"posts": posts}

    return render(request, "blog/posts.html", context)


@login_required
def ticket_upload(request):
    """
    Allows a user to upload a new ticket, including an image (optional).

    Context:
        ticket (Ticket): The newly created ticket.
        ticket_form (Form): The form for submitting a new ticket.
        photo_form (Form): The form for uploading an image.
    """
    ticket_form = forms.TicketForm
    photo_form = forms.PhotoForm
    ticket = None

    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if "image" in request.FILES:
                photo = photo_form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                ticket.image = photo

            ticket.save()
            print(f"Ticket ID: {ticket.id}")
            messages.success(request, "Votre ticket a été créé avec succès !")
            return redirect("home")
        else:
            ticket_form = forms.TicketForm()
    context = {
        "ticket": ticket,
        "ticket_form": ticket_form,
        "photo_form": photo_form,
    }
    return render(request, "blog/create_ticket.html", context=context)


@login_required
def edit_ticket(request, ticket_id):
    """
    Allows a user to edit an existing ticket, including updating its image.

    Context:
        edit_form (Form): The form for editing the ticket.
        photo_form (Form): The form for editing the ticket's image.
        ticket (Ticket): The ticket being edited.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    edit_form = forms.TicketForm(instance=ticket)
    photo_form = forms.PhotoForm(instance=ticket.image if ticket.image else None)

    if request.method == "POST":

        edit_form = forms.TicketForm(request.POST, instance=ticket)
        photo_form = forms.PhotoForm(
            request.POST,
            request.FILES,
            instance=ticket.photo if hasattr(ticket, "photo") else None,
        )

        if edit_form.is_valid():
            ticket = edit_form.save()

            photo = photo_form.save(commit=False)
            photo.ticket = ticket
            photo.uploader = request.user
            photo.save()

            ticket.image = photo
            ticket.save()

            return redirect("home")

    context = {
        "edit_form": edit_form,
        "photo_form": photo_form,
        "ticket": ticket,
    }
    return render(request, "blog/edit_ticket.html", context=context)


@login_required
def delete_ticket(request, ticket_id):
    """
    Deletes an existing ticket.

    Context:
        ticket (Ticket): The ticket to be deleted.
    """

    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        return redirect("home")


@login_required
def review_upload(request, ticket_id):
    """
    Allows a user to upload a review for a specific ticket.

    Context:
        review_form (Form): The form for submitting the review.
        ticket (Ticket): The ticket being reviewed.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a été ajoutée avec succès !")
            return redirect("home")
    else:
        review_form = forms.ReviewForm()
    context = {
        "creating_review": True,
        "review_form": review_form,
        "ticket": ticket,
    }
    return render(request, "blog/create_review.html", context=context)


@login_required
def edit_review(request, review_id):
    """
    Allows a user to edit an existing review.

    Context:
        edit_form (Form): The form for editing the review.
        review (Review): The review being edited.
        ticket (Ticket): The ticket associated with the review.
    """

    review = get_object_or_404(Review, id=review_id, user=request.user)
    edit_form = forms.ReviewForm(instance=review)
    ticket = review.ticket

    if request.method == "POST":
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect("home")

    context = {
        "creating_review": True,
        "edit_form": edit_form,
        "review": review,
        "ticket": ticket,
    }
    return render(request, "blog/edit_review.html", context=context)


@login_required
def delete_review(request, review_id):
    """
    Deletes an existing review.

    Context:
        review (Review): The review to be deleted.
    """

    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        return redirect("home")


@login_required
def create_ticket_review(request):
    """
    Allows a user to create both a ticket and a review at the same time.

    Context:
        ticket_form (Form): The form for submitting the ticket.
        photo_form (Form): The form for uploading the image for the ticket.
        review_form (Form): The form for submitting the review.
    """

    ticket_form = forms.TicketForm
    photo_form = forms.PhotoForm
    review_form = forms.ReviewForm
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if all([ticket_form.is_valid(), photo_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if "image" in request.FILES:
                photo = photo_form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                ticket.image = photo
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "Votre ticket a été créé avec succès !")
            return redirect("home")
        else:
            ticket_form = forms.TicketForm
            photo_form = forms.PhotoForm
            review_form = forms.ReviewForm

    context = {
        "ticket_form": ticket_form,
        "photo_form": photo_form,
        "review_form": review_form,
    }
    return render(request, "blog/create_ticket_review.html", context=context)


@login_required
def follow_user(request):
    """
    Allows a user to follow another user.

    Context:
        form (Form): The form for selecting a user to follow.
        followed_users (QuerySet): The list of users the current user is following.
        followers (QuerySet): The list of followers of the current user.
    """

    form = FollowUsersForm(request.POST, request_user=request.user)

    if request.method == "POST":
        if form.is_valid():
            user_to_follow = form.cleaned_data["username"]
            request.user.follows.add(user_to_follow)
            messages.success(request, f"Vous suivez maintenant {user_to_follow}.")
            return redirect("subscriptions")
        else:
            form = FollowUsersForm(request_user=request.user)

    context = {
        "form": form,
        "followed_users": request.user.follows.all(),
        "followers": request.user.followers.all(),
    }
    return render(request, "blog/subscriptions.html", context)


@login_required
def unfollow_user(request, user_id):
    """
    Allows a user to unfollow another user.

    Context:
        user_to_unfollow (User): The user to be unfollowed.
    """

    user_to_unfollow = User.objects.get(id=user_id)

    if user_to_unfollow in request.user.follows.all():
        request.user.follows.remove(user_to_unfollow)
        messages.success(request, f"Vous ne suivez plus {user_to_unfollow}.")
    else:
        messages.warning(
            request, "Cet utilisateur n'est pas dans votre liste d'abonnements."
        )

    return redirect("subscriptions")


@login_required
def subscriptions(request):
    """
    Displays a list of users the current user follows and who follows them.

    Context:
        following (QuerySet): The list of users the current user is following.
        followers (QuerySet): The list of users following the current user.
        form (Form): The form to follow other users.
    """

    following = request.user.follows.all()
    followers = request.user.followers.all()
    form = FollowUsersForm(request.POST, request_user=request.user)

    print("Following:", following)
    print("Followers:", followers)

    context = {"following": following, "followers": followers, "form": form}

    return render(request, "blog/subscriptions.html", context)
