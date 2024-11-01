from django.db import models
from auths.models import User

# Create your models here.

class Chat(models.Model):
    idChat = models.AutoField(primary_key=True)
    dateAdd = models.DateTimeField(auto_now_add=True)
    dateModif = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_as_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_as_user2")
    
    class Meta:
        unique_together = ('user1', 'user2')  # Ensure each pair of users has only one chat

    def __str__(self):
        return f"Chat between {self.user1.pseudoUser} and {self.user2.pseudoUser}"

class MessageChat(models.Model):
    idMes = models.AutoField(primary_key=True)
    descriptMes = models.TextField()
    dateAdd = models.DateTimeField(auto_now_add=True)
    dateModif = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.idMes
