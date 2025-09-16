from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Project
from .forms import ProjectForm, UserRegistrationForm


def index(request):
    return render(request, 'index.html')


def project_list(request):
    query = request.GET.get("q")
    project_list = Project.objects.all().order_by('-created_at')

    # 🔍 Search
    if query:
        project_list = project_list.filter(
            Q(text__icontains=query) | Q(user__username__icontains=query)
        )

    # 📄 Pagination (6 per page)
    paginator = Paginator(project_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'project_list.html', {
        "projects": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "query": query,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id, user=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'project_confirm_delete.html', {'project': project})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
