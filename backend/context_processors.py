from .models import *
from django.shortcuts import render
import random

def Collection(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user.id)
    else:
        cart_items = []
    collection = Products.objects.all()[:9]
    new_products = Products.objects.all().order_by('-id')[:6]
    products = Products.objects.all()
    new_newsletters = Newsletters.objects.filter(is_approved = False)
    new_contactforms = Contact.objects.filter(is_read = False)
    new_orders = Orders.objects.filter(is_completed = False)
    new_reviews = Reviews.objects.filter(is_read = False)
    notifications = len(new_newsletters) + len(new_contactforms) + len(new_reviews) + len(new_orders)
    best_seller  = Products.objects.filter(is_best_selling = True)
    recommended_products = Products.objects.all()
    if len(recommended_products)>3:
        recommended_products = random.sample(list(recommended_products),3)
    images = Images.objects.all()
    first_images = []
    cart_products = []
    cart_total = 0
    if request.user.is_authenticated:
        cart_products = Cart.objects.filter(user = request.user.id)
        for product in cart_products:
            cart_total = cart_total + int(product.total)
    for product in Products.objects.all():
        image = images.filter(product = product.id).first()
        first_images.append(image)
    new_arrivals = Products.objects.filter(is_published = True).filter(is_new_arrival = True)[:4]
    company = Company.objects.first()
    categories = ProductCategory.objects.filter(show_on_home = True)[:6]
    banners = Banner.objects.all().order_by('id')
    context = {
        "collection":collection,
        "company":company,
        "categories":categories,
        "banners":banners,
        "images":images,
        "new_products":new_products,
        'first_images':first_images,
        "cart_products":cart_products,
        "cart_number":len(cart_products),
        "products":products,
        "notifications":notifications,
        "new_newsletters":len(new_newsletters),
        "recommended_products":recommended_products,
        "new_contactforms":len(new_contactforms),
        "new_reviews":len(new_reviews),
        "cart_items":len(cart_items),
        "cart_total":cart_total,
        "new_orders":len(new_orders),
        "new_arrivals":new_arrivals,
        "best_seller":best_seller,
        "best_seller_footer":best_seller[:2],
    }

    return context
