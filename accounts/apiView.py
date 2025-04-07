import openmeteo_requests
import requests_cache
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from retry_requests import retry
from django.http import JsonResponse

def apiV