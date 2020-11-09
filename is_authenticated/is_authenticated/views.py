from django.http import HttpResponse

def is_authenticated(request):
    if request.user.is_authenticated:
        return HttpResponse('Signed in')
    else:
        return HttpResponse('Not signed in!', status=401)
