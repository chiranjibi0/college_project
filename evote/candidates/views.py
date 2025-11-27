from django.shortcuts import render,get_object_or_404,redirect 
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
import logging
from django.db import transaction

# Create your views here.

def show_candidate(request):
    candidate=Candidate.objects.all()
    context={
        'candidate':candidate,

    }
    return render(request, 'show_candidates.html',context)
def show_party(request):
    party=Candidate.objects.value('party_name')
    context={
        'party':party,

    }
    return render(request, 'show_candidates.html',context)

def show_voters(request):
    voters=Voter.objects.all()
    context={
        'voters':voters
    }
    return render(request, 'show_voters.html',context)


def show_election(request):
    election=Election.objects.values('election_name', 'start_date', 'end_date', 'notes')
    context={
        'election':election
    }
    return render(request, 'show_election.html',context)
    

def show_result(request):
    result=Election.objects.all()
    context={
        'result':result
    }
    return render(request, 'show_result.html',context)


def vote_candidate(request, candidate_id):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('show_candidate')

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to vote.")
        return redirect('show_voters')

    candidate = get_object_or_404(Candidate, id=candidate_id)

    try:
        current_voter = Voter.objects.get(voter_name=request.user.username)
    except Voter.DoesNotExist:
        messages.error(request, "Voter account not found for the logged-in user.")
        return redirect('show_voters')

    # Check if the voter has already voted
    if Vote.objects.filter(voter=current_voter).exists():
        messages.warning(request, "You have already voted.")
        return redirect('show_candidate')

    try:
        # Try to create a vote atomically
        with transaction.atomic():
            # Create the vote
            vote = Vote.objects.create(
                voter=current_voter,
                candidate=candidate
            )

            # Increment the vote count for the candidate
            candidate.vote = F('vote') + 1  # Use F() expression for efficient DB update
            candidate.save()

        messages.success(request, f"Successfully voted for {candidate.candidate_name}!")
    except Exception as e:
        messages.error(request, "An unexpected error occurred while processing your vote.")
        logging.error(f"Error occurred while voting: {e}")

    return redirect('show_candidate')
