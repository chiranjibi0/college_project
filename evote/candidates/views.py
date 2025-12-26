from django.shortcuts import render,get_object_or_404,redirect 
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
import logging
from django.db import transaction
from django.db import IntegrityError

# Create your views here.
def show_candidate(request):
    candidates = Candidate.objects.all()
    voted_candidate_id = None

    if request.user.is_authenticated:
        voter = Voter.objects.filter(voter_name=request.user.username).first()
        if voter:
            vote = Vote.objects.filter(voter=voter).first()
            if vote:
                voted_candidate_id = vote.candidateId.id

    return render(request, 'show_candidates.html', {
        'candidate': candidates,
        'voted_candidate_id': voted_candidate_id
    })


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
        return redirect('show_candidate')

    if not request.user.is_authenticated:
        messages.error(request, "Please login to vote.")
        return redirect('login')

    voter = Voter.objects.filter(voter_name=request.user.username).first()
    if not voter:
        messages.error(request, "No voter account linked with you.")
        return redirect('show_candidate')

    if Vote.objects.filter(voter=voter).exists():
        messages.warning(request, "You have already voted.")
        return redirect('show_candidate')

    candidate = get_object_or_404(Candidate, id=candidate_id)

    try:
        with transaction.atomic():
            Vote.objects.create(voter=voter, candidateId=candidate)
            Candidate.objects.filter(id=candidate.id).update(voteCount=F('voteCount') + 1)

        messages.success(request, "Vote recorded successfully.")

    except IntegrityError:
        messages.warning(request, "You have already voted.")

    except Exception as e:
        print("Vote error:", e)
        messages.error(request, "Vote failed.")

    return redirect('show_candidate')

