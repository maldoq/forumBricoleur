from django.db import models
from auths.models import User

# Create your models here.

class Tag(models.Model):
    idTag = models.AutoField(primary_key=True)
    libelleTag = models.CharField(max_length=50)

    def __str__(self):
        return self.libelleTag


class Article(models.Model):
    idArt = models.AutoField(primary_key=True)
    imageArt = models.ImageField(upload_to="images/article/")
    titreArt = models.CharField(max_length=100)
    descriptArt = models.TextField()
    dateArt = models.DateTimeField(auto_now_add=True)
    dateModif = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.titreArt
    
    def comment_count(self):
        return self.comment_set.count()

    def like_count(self):
        return self.like_set.filter(liked=True).count()

    def dislike_count(self):
        return self.dislike_set.filter(disliked=True).count()
    
class ArticleItem(models.Model):
    idArtItem = models.AutoField(primary_key=True)
    titreArt = models.CharField(max_length=100, default='')
    descriptArt = models.TextField(default='')
    dateAdd = models.DateTimeField(auto_now_add=True)
    dateModif = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=None)

class Comment(models.Model):
    idCom = models.AutoField(primary_key=True)
    descriptCom =models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.idCom)

class Like(models.Model):
    idLike = models.AutoField(primary_key=True)
    liked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.idLike)

class DisLike(models.Model):
    idDis = models.AutoField(primary_key=True)
    disliked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.idDis