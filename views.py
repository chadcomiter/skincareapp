from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Product, Ingredient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm, CreateIngredientForm, CreateProductForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import Lower
from operator import itemgetter

# Create your views here.


##Homepage
def home(request):
    return render(
                request = request,
                template_name = "main/home.html")


##Handles User Stuff

##Registration View
def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("/")
        
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            
            return render(
                request = request,
                template_name = "main/register.html",
                context={"form":form})

    form = NewUserForm
    return render(request = request,
    template_name = "main/register.html",
    context={"form":form})

##Logout 
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

##Support
def support(request):
    return render(
        request=request,
        template_name="main/support.html"
    )

##Login
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/product_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

##CRUD

##Create Product
'''class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'breakout']
    success_url='/product_list'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)'''

def create_product(request):
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('product_list')


    return render(
        request = request,
        template_name='main/create_product.html',
        context={"form":form})

##Create Ingredient
def create_ingredient(request):
    form = CreateIngredientForm()
    if request.method == 'POST':
        form = CreateIngredientForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('/create_ingredient')
    
    return render(
        request = request,
        template_name='main/create_ingredient.html',
        context={"form":form})
 
##List View of Products
def product_list(request):
    return render(request,
    "main/product_list.html", 
    context={"products":Product.objects.filter(user=request.user)}
    )

##Detailed Product View
class ProductDetailView(DetailView):
    model = Product

##Update Product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'breakout']
    success_url='/product_list'

##Delete Product
class ProductDeleteView(DeleteView):
    model = Product
    success_url='/product_list'

##Delete Ingredient
class IngredientDeleteView(DeleteView):
    model = Ingredient
    success_url='/product_list'




##Classifier
def classifier(request):
    ##Get all the ingredients in all of the breakout products for the user
    br_ingredients = Ingredient.objects.filter(product__in=Product.objects.filter(user=request.user, breakout=True)).values_list(Lower('name')).annotate(num = Count('name'))
    ##Get all the ingredients in all of the non-breakout products for the user
    nbr_ingredients = Ingredient.objects.filter(product__in=Product.objects.filter(user=request.user, breakout=False)).values_list(Lower('name')).annotate(num = Count('name'))
    
    ##Get the total number of ingredients in each category
    total_br = Ingredient.objects.filter(product__in=Product.objects.filter(user=request.user, breakout=True)).count()
    total_nbr = Ingredient.objects.filter(product__in=Product.objects.filter(user=request.user, breakout=False)).count()

    ##Calculate the classifier score for each ingredient & store as a tuple w/ ingredient name and score ie. [[ingredient, 0.2], [ingredient_2, 0.4],...]
    br_score= []
    for i in br_ingredients:
        score = (i[1]/total_br)
        br_score.append([i[0], score])
    
    nbr_score = []
    for i in nbr_ingredients:
        score = (i[1]/total_nbr)
        nbr_score.append([i[0], score])

    ##Sort the items in the breakout category by descending integer order
    desc_br_ingredients = sorted(br_score, key=itemgetter(1), reverse=True)
    

    ##Search the breakout ingredients to find ones that do not occur in safe products
    br_names = []
    nbr_names = []
    for i in br_score:
        br_names.append(i[0])
    for i in nbr_score:
        nbr_names.append(i[0])
    
    danger_products = list(set(br_names) - set(nbr_names))

  
    return render(request = request,
                    template_name = "main/classifier.html",
                    context = {"br_ingredients": br_ingredients, 
                    "nbr_ingredients": nbr_ingredients, 
                    "total_br": total_br, 
                    "total_nbr": total_nbr, 
                    "br_score": br_score,
                    "nbr_score": nbr_score,
                    "danger_products": danger_products,
                    "descending_breakout": desc_br_ingredients,
                    })
    

   


