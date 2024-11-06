from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from auths.models import User
from django.contrib import messages
from .models import Article,Tag,Comment, Like, DisLike
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

# Create your views here.

def index(request):
    # verifie si la session contient 'user_id' et 'otp'
    # if 'user_id' not in request.session:
    #     # Sinon, renvoyer l'utilisateur sur la page de connection avec un message d'erreur
    #     messages.warning(
    #         request,
    #         'You must log in first.',
    #     )
    #     return redirect('login')
    articles = Article.objects.filter(status=True)
    is_connected = False
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        is_connected = True
        context = {"user":user, "articles":articles[:6],"is_connected":is_connected}
    else:
        is_connected = False
        context={"articles":articles[:6],"is_connected":is_connected}
    return render(request,"index.html", context)

def blog(request):
    tags = Tag.objects.all()
    articles = Article.objects.filter(status=True)
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        context = {"user":user, "articles":articles,"tags":tags}
    else:
        context={"articles":articles,"tags":tags}
    return render(request,"contain/article.html", context)

def blog_detail(request,idArt):
    article = Article.objects.get(idArt=idArt)
    comments = Comment.objects.filter(article=article)
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        context = {"user":user, "article":article,"comments":comments}
    else:
        context={"article":article,"comments":comments}
    return render(request,"contain/article_detail.html", context)

@csrf_protect
def add_comment(request,idArt):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        article = Article.objects.get(idArt=idArt)

        if request.method == "POST":
            message = request.POST["message"]

            # liste vide d'erreur qui sera affiche sur le site
            error_fields = []

            if message is None or message =='':
                messages.error(request, 'aucun message entré.')
                error_fields.append('message')

            # si la liste d'erreur n'est pas vide, renvoyer le sur le site
            if error_fields:
                context = {"user":user, "article":article,'error_fields': error_fields}
                return render(
                    request, 'contain/article_detail.html', context
                )
            
            new_comment = Comment(
                descriptCom = message,
                user = user,
                article = article
            )
            new_comment.save()
            context = {"user":user, "article":article}
            return redirect('blog_detail', idArt=article.idArt)
    else:
        return redirect("login")
    
@csrf_protect
def like_article(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        article = Article.objects.get(idArt=article_id)

        like, created = Like.objects.get_or_create(user=user, article=article)
        if created:
            like.liked = True
            like.save()
            # Remove any existing dislikes
            DisLike.objects.filter(user=user, article=article).delete()
            return JsonResponse({'success': True, 'like_count': article.like_count(), 'dislike_count': article.dislike_count()})
        else:
            like.delete()
            return JsonResponse({'success': True, 'like_count': article.like_count(), 'dislike_count': article.dislike_count()})
    else:
        return JsonResponse({'success': False, 'error': 'User not logged in'})

@csrf_protect
def dislike_article(request, article_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        article = Article.objects.get(idArt=article_id)

        dislike, created = DisLike.objects.get_or_create(user=user, article=article)
        if created:
            # Remove any existing likes
            Like.objects.filter(user=user, article=article).delete()
            dislike.disliked = True
            dislike.save()
            return JsonResponse({'success': True, 'like_count': article.like_count(), 'dislike_count': article.dislike_count()})
        else:
            dislike.delete()
            return JsonResponse({'success': True, 'like_count': article.like_count(), 'dislike_count': article.dislike_count()})
    else:
        return JsonResponse({'success': False, 'error': 'User not logged in'})

def myblog(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        articles = Article.objects.filter(user=user)
        context= {"user":user,"articles":articles}
        return render(request,"contain/myblog.html",context)
    else:
        return redirect('login')

def myblog_article_detail(request, action):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        tags = Tag.objects.all()

        if action == 'add':
            title = "Ajout d'un nouvel article"
            context = {"user":user,"title":title,"tags":tags}
        return render(request,'contain/myblog_article_detail.html',context)
    
def add_article(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
    if request.method == "POST":
        image =  request.FILES['image']
        titre = request.POST['title']
        tag_id = request.POST['tag']
        descript = request.POST['descript']

        tag = Tag.objects.get(idTag=tag_id)

        new_article = Article(
            imageArt = image,
            titreArt = titre,
            descriptArt = descript,
            tag = tag,
            user = user
        )
        new_article.save()
        return redirect(reverse('myblog'))
    
def myblog_article_detail_edit(request, action, idArt):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = User.objects.get(idUser=user_id)
        article = Article.objects.get(idArt=idArt)
        tags = Tag.objects.all()  # Get all tags for the select input

        if action == 'edit':
            title = "Modification d'un article"
            context = {
                "user": user,
                "title": title,
                "article": article,
                "tags": tags,
                "action": action  # Add the action to the context
            }
        elif action == 'show':
            title = "Consultation d'un article"
            context = {
                "user": user,
                "title": title,
                "article": article,
                "action": action
            }
        return render(request, 'contain/myblog_article_detail.html', context)
    
def edit_article(request, idArt):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')
    user = get_object_or_404(User, idUser=user_id)
    article = get_object_or_404(Article, idArt=idArt)
    tags = Tag.objects.all()  # Get all tags for the dropdown

    if request.method == "POST":
        # Handle file uploads properly if 'image' is a file
        if 'image' in request.FILES:
            article.imageArt = request.FILES['image']
        else:
            article.imageArt = request.POST.get('image', article.imageArt)

        article.titreArt = request.POST.get('title', article.titreArt)
        tag_id = request.POST.get('tag')
        article.tag = Tag.objects.get(idTag=tag_id) if tag_id else article.tag
        article.descriptArt = request.POST.get('descript', article.descriptArt)
        article.user = user

        article.save()
        return redirect(reverse('myblog'))


def show_article(request,idArt):
    pass

def delete_article(request,idArt):
    pass

