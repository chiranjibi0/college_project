from django.db import models

# Create your models here.
class Party(models.Model):
    party_name=models.CharField(max_length=50)
    party_image=models.ImageField()    
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.party_name
    
class Candidate(models.Model):
    candidate_name=models.CharField(max_length=100)
    candidate_age=models.IntegerField()
    candidate_image=models.FileField(upload_to='static/uploads',null=True)
    candidate_number=models.BigIntegerField()
    candidate_slogan=models.TextField()
    voteCount=models.IntegerField(default=0)
    party=models.ForeignKey(Party,on_delete=models.CASCADE)

    def __str__(self):
        return self.candidate_name
    
class Voter(models.Model):
    voter_name=models.CharField(max_length=100)
    voter_id_number=models.BigIntegerField()
    voter_age=models.IntegerField()

    def __str__(self):
        return self.voter_name
    
class Election(models.Model):
    election_name=models.CharField(max_length=100 ,null=True)
    start_date=models.DateField()
    end_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    notes=models.CharField(max_length=100)

    def __str__(self):
        return self.notes
    
class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidateId = models.ForeignKey(Candidate, on_delete=models.CASCADE, default=None, null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter',)

        
    def __str__(self):
        return f"{self.voter.voter_name} voted for {self.candidateId.candidate_name}"

