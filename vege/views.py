from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import Recipe

def login_page(request):
    if request.method == "POST":
        username_ = request.POST.get("username")
        password_ = request.POST.get("password")

        if User.objects.filter(username = username_).exists():
            user = authenticate(username=username_,password = password_)
            if user:
                login(request,user)
                return redirect("dashboard")
            else:
                messages.error(request,"Invalid Credential")
        else:
            messages.error(request,"User not exists")
    return render(request,'vege/login.html')
    
@login_required(login_url="login_page")
def logout_page(request):
    logout(request)
    return redirect("login_page")

def register_page(request):
    if request.method == "POST":
        username_ = request.POST.get("username")
        fname_ = request.POST.get("fname")
        lname_ = request.POST.get("lname")
        password_ = request.POST.get("password")

        if User.objects.filter(username = username_).exists():
            messages.error(request,"this username is already taken")
        else:
            new_user = User(
                username = username_,
                first_name = fname_   ,
                last_name = lname_
            )
            new_user.set_password(password_)

            new_user.save()
            messages.success(request,'Register Successfully')
            return redirect("login_page")

    return render(request,'vege/register.html')

@login_required(login_url="login_page")
def dashboard(request):
    queryset = Recipe.objects.all()
    if request.method == "POST":
        rname_ = request.POST.get("rname")
        dname_ = request.POST.get("dname")
        rimage_ = request.FILES.get("rimage")
        print(rimage_,'--------------------------')
        if not rname_ or not dname_ or not rimage_:
            messages.error(request,"Error")
        else:    
            Recipe.objects.create(
                recipe_name = rname_,
                recipe_description = dname_,
                recipe_image = rimage_       
            )
            messages.success(request,"Recipe added successfully")
            return redirect('dashboard')

    search_ = request.GET.get("search")    
    if search_:
        queryset = queryset.filter(recipe_name__icontains = search_)
    
    context = {
        "recipes" : queryset
    }
    return render(request,'vege/dashboard.html',context)

@login_required(login_url="login_page")
def update_recipe(request,id):
    myrecipe = Recipe.objects.get(id=id)
    context = {
        "recipe" : myrecipe
    }
    if request.method == "POST":
        rname_ = request.POST.get("rname")
        dname_ = request.POST.get("dname")
        rimage_ = request.FILES.get("rimage")

        if rname_:
            myrecipe.recipe_name = rname_
        if dname_:
            myrecipe.recipe_description = dname_
        if rimage_:
            myrecipe.recipe_image = rimage_
        myrecipe.save()
        messages.success(request,"Recipe Updated Successfully")

    return render(request,'vege/update.html',context)
    
@login_required(login_url="login_page")
def delete_recipe(request,id):
    myrecipe = Recipe.objects.get(id=id)
    myrecipe.delete()
    messages.success(request,"Recipe deleted successfully")
    return redirect('dashboard')