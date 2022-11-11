from django.contrib.auth import authenticate

def authenticate_service(request, data):
    username = data['username']
    password = data['password']
    user = authenticate(
        request, 
        username=username, 
        password=password
    )
    return user