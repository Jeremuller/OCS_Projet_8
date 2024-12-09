from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm


@login_required
def home(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-time_created')
    return render(request, 'blog/home.html', {'tickets': tickets})


@login_required
def ticket_upload(request):
    ticket_form = TicketForm
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket_form.save()
            messages.success(request, "Votre ticket a été créé avec succès !")
            return redirect('home')
        else:
            ticket_form = TicketForm()
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'blog/create_ticket.html', context=context)
