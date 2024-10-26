from django.shortcuts import render,redirect
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import generics
from .models import Client, Project
from .serializers import Client_S, Project_S, User_S
from .models import User
from rest_framework.permissions import AllowAny
from django.views.generic import TemplateView
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

class CreateUser(generics.ListCreateAPIView):  # Follow PEP 8 naming conventions
    queryset = User.objects.all()
    serializer_class = User_S
    permission_classes = [AllowAny]

class UpdateDelUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = User_S


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('login')  # Redirect to the login page or your desired page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form}) 

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your login template here

    def get_success_url(self):
        return reverse_lazy('create-users') 

class CreateClients(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = Client_S
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username)  # Automatically set created_by

class UpdateDelClients(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = Client_S

class CreateProjects(generics.ListCreateAPIView):
    serializer_class = Project_S

    def perform_create(self, serializer):
        client_id = self.kwargs.get('id')  # Retrieve client id from URL
        client = Client.objects.get(id=client_id)  # Get client object
        serializer.save(client=client)  # Save project with associated client

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(users=user)  # List projects assigned to logged-in user

class UpdateDelProjects(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = Project_S


class RegistrationView(TemplateView):
    template_name = 'register.html'