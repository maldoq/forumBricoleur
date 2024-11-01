from django.db import models

# Create your models here.

class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    pseudoUser = models.CharField(max_length=40)
    nomUser = models.CharField(max_length=30)
    prenomsUser = models.CharField(max_length=50)
    emailUser = models.CharField(max_length=100)
    motPassUser = models.CharField(max_length=100)
    dateNaissUser = models.DateField()
    avatarUser = models.ImageField(upload_to="images/profilUser/")
    dateAdd = models.DateTimeField(auto_now_add=True)
    dateModif = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.pseudoUser

class Subscribe(models.Model):
    idAbon = models.AutoField(primary_key=True)
    dateAbon = models.DateTimeField(auto_now_add=True)
    suivi = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user_followed")
    abonne = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="user_follow_you")

    def __str__(self):
        return f"{self.idAbon} | {self.dateAbon}"