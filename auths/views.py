from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def login(request):

    if request.method == "POST":
        pseudo = request.POST['pseudo']
        password = request.POST['pass']

        # liste vide d'erreur qui sera affiche sur le site
        error_fields = []

        try:
            # verification de l'email dans la base de donnees
            user = User.objects.get(pseudoUser=pseudo)

            if user.motPassUser == password:
                request.session['user_id'] = user.idUser

                return redirect('home')
            else:
                messages.error(request, 'Mot de passe invalid.')
                error_fields.append('pass')
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist.')
            error_fields.append('pseudo')
        # Return errors if any
        return render(request, 'auth/connexion.html', {'error_fields': error_fields})
    return render(request,'auth/connexion.html')

@csrf_protect
def signup(request):
    if request.method == "POST":
        profil = request.FILES.get('image', None)
        pseudo = request.POST['pseudo']
        lastName = request.POST['lastname']
        firstName = request.POST['firstname']
        email = request.POST['email']
        date = request.POST['date']
        password = request.POST['pass1']
        cpassword = request.POST['pass2']

        error_fields = []

        # Password match validation
        if password != cpassword:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            error_fields.extend(['pass1', 'pass2'])

        # Email uniqueness validation
        if User.objects.filter(emailUser=email).exists():
            messages.error(request, 'Un utilisateur avec cet email existe déjà.')
            error_fields.append('email')

        # Pseudo uniqueness validation
        if User.objects.filter(pseudoUser=pseudo).exists():
            messages.error(request, 'Un utilisateur avec ce pseudo existe déjà.')
            error_fields.append('pseudo')

        if error_fields:
            return render(request, 'auth/inscription.html', {'error_fields': error_fields})

        new_user = User(
            avatarUser=profil,
            pseudoUser=pseudo,
            nomUser=lastName,
            prenomsUser=firstName,
            emailUser=email,
            motPassUser=password,
            dateNaissUser=date,
        )
        new_user.save()
        return redirect('login')

    return render(request, 'auth/inscription.html')


def logout(request):
    # Remove the session key
    if 'user_id' in request.session:
        del request.session['user_id']
    # Redirect to the login page
    return redirect('home')