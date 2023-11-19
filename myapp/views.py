from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.models import Books

from myapp.forms import BookForm,BookModelForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper 

@method_decorator(signin_required,name="dispatch")       
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BookModelForm()
        return render(request,"book_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=BookModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book has been added")
            # print(form.cleaned_data)
            # Books.objects.create(**form.cleaned_data)
            print("created")
            return render(request,"book_add.html",{"form":form})
        else:
            messages.error(request,"failed to create book")
            return render(request,"book_add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")       
class BookListView(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
        categories=Books.objects.all().values_list("category",flat=True).distinct()
        print(categories)
        if "category" in request.GET:
            catg=request.GET.get("category")
            qs=qs.filter(category__iexact=catg)

        return render(request,"book_list.html",{"data":qs,"categories":categories})
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Books.objects.filter(bookname__icontains=name,)
        return render(request,"book_list.html",{"data":qs})
        

@method_decorator(signin_required,name="dispatch")       
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        print(kwargs)
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,"book_detail.html",{"data":qs})


@method_decorator(signin_required,name="dispatch")       
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        messages.success(request,"Deleted")
        return redirect("book-all")

@method_decorator(signin_required,name="dispatch")          
class BookUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookModelForm(instance=obj)
        return render(request,"book_edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book changed")
            return redirect("book-details",pk=id)
        else:
            messages.error(request,"failed to update")
            return render(request,"book_edit.html",{"form":form})
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"created")
            # print("saved")
            return render(request,"register.html",{"form":form})
        else:
            # print("failed")
            messages.error(request,"failed")
            return render(request,"register.html",{"form":form})
          
 

class SignInView(View):

    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():

            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(u_name,pwd)
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                print("valid credential")
                login(request,user_obj)
                messages.success(request,"valid credential")
                return redirect("book-all")
                
            # else:
            #     print("invalid credential")

            return render(request,"login.html",{"form":form})
        else:
            messages.error(request,"invalid credential")
            return render(request,"login.html",{"form":form})


@method_decorator(signin_required,name="dispatch")       
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin") 

   
           
                
           


        
        

