from django.shortcuts import render,redirect
from backend.models import *
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    return render(request,"homepage/index.html")

def ContactUs(request):
    return render(request,"contact/contact-page.html")

def Shop(request):
    query = request.GET.get('search')
    products = Products.objects.filter(is_published =True)
    if query:
        products = Products.objects.filter(Q(name__icontains = query) | Q(category__name__icontains = query) | Q(tags__icontains = query))
    products_per_page = 10
    paginator = Paginator(products, products_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"shop/shop.html",{'shop_products': page_obj,"total_products":len(products),"products_per_page":products_per_page})


def Checkout(request):
    return render(request,"checkout/checkout.html")

def UserCart(request):
    if request.user.is_authenticated:
        addresses = UserAddress.objects.filter(user = request.user.id)
        return render(request,"cart/cart.html",{"addresses":addresses})
    return redirect('login')

def ShopDetails(request,product_id):
    product = Products.objects.filter(id = product_id).first()
    product_images = Images.objects.filter(product = product_id)
    product_reviews = Reviews.objects.filter(product = product_id)
    related_products = Products.objects.filter(Q(category__name__icontains = product.category.name) | Q(tags__icontains = product.tags) | Q(name__icontains = product.name))
    return render(request,"shop/shop-details.html",{"product":product,"product_images":product_images,"product_reviews":product_reviews,"related_products":related_products})

def Post(request):
    return render(request,"post/post.html")


def About(request):
    return render(request,"aboutus/about-page.html")


def Blogs(request):
    return render(request,"blogs/blogs-page.html")