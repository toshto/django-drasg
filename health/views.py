from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection


def check(request):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 AS DUMMY")
    row = cursor.fetchone()
    return HttpResponse(row)
