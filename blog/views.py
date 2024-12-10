from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Review
from . import forms


@login_required
def home(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    tickets_with_reviews = []

    for ticket in tickets:
        ticket_reviews = Review.objects.filter(ticket=ticket)
        tickets_with_reviews.append({
            'ticket': ticket,
            'reviews': ticket_reviews,
        })
    context = {
        'tickets_with_reviews': tickets_with_reviews,
        'reviews': reviews,
    }
    return render(request, 'blog/home.html', context)


@login_required
def ticket_upload(request):
    ticket_form = forms.TicketForm
    photo_form = forms.PhotoForm
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), photo_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if 'image' in request.FILES:
                photo = photo_form.save(commit=False)
                photo.uploader = request.user
                photo.save()
                ticket.image = photo

            ticket.save()
            messages.success(request, "Votre ticket a été créé avec succès !")
            return redirect('home')
        else:
            ticket_form = forms.TicketForm()
    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
    }
    return render(request, 'blog/create_ticket.html', context=context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()

    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST,instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        elif 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def review_upload(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a été ajoutée avec succès !")
            return redirect('home')
    else:
        review_form = forms.ReviewForm()
    context = {
        'review_form': review_form,
        'ticket': ticket,
    }
    return render(request, 'blog/create_review.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()

    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST,instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        elif 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')

    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_review.html', context=context)


@login_required
def create_ticket_review(request):
    ticket_form = forms.TicketForm
    photo_form = forms.PhotoForm
    review_form = forms.ReviewForm
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if all([ticket_form.is_valid(), photo_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if 'image' in request.FILES:
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
            return redirect('home')
        else:
            ticket_form = forms.TicketForm
            photo_form = forms.PhotoForm
            review_form = forms.ReviewForm

    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
        'review_form': review_form,
    }
    return render(request, 'blog/create_ticket_review.html', context=context)
