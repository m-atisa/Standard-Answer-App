from django.shortcuts import render
from django.db.models import Q
from .models import ExcelDocument
# Create your views here.
def get_file_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        files = ExcelDocument.objects.filter(
            Q(title__icontains=q),
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))