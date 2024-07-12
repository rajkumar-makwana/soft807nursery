from django.contrib.auth import login,logout,authenticate,get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
import os



# =================== Others ======================

User = get_user_model()

def is_admin(request):
    if request.user.is_superuser:
        return True
    return False

def is_loggin(request):
    if request.user.is_authenticated:
        return True
    return False

def is_method_post(request):
    if request.method == "POST":
        return True
    return False

def Error404(request):
    return render(request,"error/404.html")

def Error500(request):
    return render(request,"error/500.html")

def AdminDashboard(request):
    if is_admin(request):
        return render(request,"homepage/admin_dashboard.html")
    return redirect('404')




# ===================== All ========================

def AllProducts(request):
    if is_admin(request):
        products = Products.objects.all()
        product_images = Images.objects.all()
        context = {
            "products":products,
            "images":product_images
        }
        return render(request,'all/products.html',context)

def AllBanners(request):
    if is_admin(request):
        banners = Banner.objects.all()
        return render(request,"all/banner.html",{"banners":banners})
    return redirect('404')

def AllNewsletters(request):
    if is_admin(request):
        newsletters = Newsletters.objects.all()
        return render(request,"all/newsletters.html",{"newsletters":newsletters})

def AllReviews(request):
    if is_admin(request):
        reviews = Reviews.objects.all()
        return render(request,"all/reviews.html",{"reviews":reviews})

def AllContactForms(request):
    if is_admin(request):
        
        contactforms = Contact.objects.all()
        return render(request,"all/contactforms.html",{"contactforms":contactforms})

def AllOrders(request):
    if is_loggin(request):
        if is_admin(request):
            orders = Orders.objects.all()
            return render(request,"all/admin-orders.html",{"orders":orders})
        orders = Orders.objects.filter(user = request.user.id)

        return render(request,"all/orders.html",{"orders":orders})
    return redirect('login')

def ViewCart(request):
    if is_loggin(request):
        addresses = UserAddress.objects.filter(user = request.user.id)
        cart_items = Cart.objects.filter(user = request.user.id)
        total = 0
        for item in cart_items:
            total = total + (int(item.quantity) * int(item.product.selling_price.replace('₹','')))
        return render(request,"all/cart.html",{"cart_items":cart_items,"total":total,"addresses":addresses})
    return redirect('login')

def AllBlogs(request):
    blogs = Blogs.objects.all()
    return render(request,"all/blogs.html",{"blogs":blogs})

def AllBlogComments(request):
    if is_admin(request):
        blog_comments = BlogComments.objects.all()
        return render(request,"all/blog_comments.html",{"blog_comments":blog_comments})
    return redirect('404')


# =================== Add =========================

def AddCompany(request):
    if is_admin(request):
        form = CompanyForm()
        existing_company = Company.objects.all()
        if existing_company.exists():
            return redirect('edit-company')
        if is_method_post(request):
            
            form = CompanyForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,"Added")
                return redirect('edit-company')
        return render(request,"add/company.html")
    return redirect('404')
            # company = Company.objects.create(
            #     name = request.POST.get('name'),
            #     description = request.POST.get('description'),
            #     email = request.POST.get('email'),
            #     phone_number = request.POST.get('phone_number'),
            #     logo = request.FILES.get('logo'),
            #     favicon = request.POST.get('favicon'),
            #     address = request.POST.get('address'),
            # )

def AddCategory(request):
    if is_admin(request):
        categories = ProductCategory.objects.all()
        if is_method_post(request):
            try:
                category = ProductCategory.objects.create(
                    name = request.POST.get('category_name'),
                    image = request.FILES.get('image'),
                    show_on_home = request.POST.get('show_on_home') if request.POST.get('show_on_home') else 0,
                )
                category.save()
                return redirect('all-categories')
            except Exception as e:
                category.delete()
        return render(request,'all/categories.html',{"categories":categories})
    return redirect('404')

def AddProduct(request):
    if is_admin(request):
        if is_method_post(request):
            try:
                name = request.POST.get('name')
                category = request.POST.get('category')
                cost_price = request.POST.get('cost_price')
                selling_price = request.POST.get('selling_price')
                short_description = request.POST.get('short_description')
                description = request.POST.get('description')
                tags = request.POST.get('tags')
                is_published = request.POST.get('is_published')
                is_new_arrival = request.POST.get('is_new_arrival')
                is_best_selling = request.POST.get('is_best_selling')
                

                product = Products.objects.create(
                    name = name,
                    category_id = category,
                    cost_price = cost_price,
                    selling_price = selling_price,
                    short_description = short_description,
                    description = description,
                    tags = tags,
                    is_published = is_published,
                    is_new_arrival = request.POST.get('is_new_arrival'),
                    is_best_selling = request.POST.get('is_best_selling'),
                )
                product.save()
                images = request.FILES.getlist('images')
                try:
                    for image in images:
                        img = Images.objects.create(
                            image = image,
                            product_id = product.id
                        )
                        img.save()
                except Exception as e:
                    product.delete()
                messages.success(request,"added")
                return redirect('add-product')
            except Exception as e:
                print(e)
                return redirect('add-product')
        return render(request,"add/product.html")
    return redirect('404')

def AddBanner(request):

    if is_admin(request):
        if is_method_post(request):
            banner = Banner.objects.create(
                image = request.FILES.get('image'),
                title = request.POST.get('title'),
                heading = request.POST.get('heading'),
                sub_heading = request.POST.get('sub_heading')
            )
            banner.save()
            messages.success(request,'✔️')
            return redirect('add-banner')
        return render(request,"add/banner.html")
    return redirect('404')

def AddToCart(request):
    if is_loggin(request):
        if is_method_post(request):
            product = Products.objects.filter(id = request.POST.get('product_id')).first()
            existing_data = Cart.objects.filter(user = request.user.id).filter(product = request.POST.get('product_id'))
            if existing_data.first():
                cart = existing_data.update(
                    quantity = request.POST.get('quantity') if request.POST.get('quantity') else int(existing_data.first().quantity) + 1,
                )
                qunt = existing_data.first().quantity
                cart = existing_data.update(
                    total = int(product.selling_price) * int(qunt)
                )

                return redirect(request.META.get('HTTP_REFERER'))
            cart = Cart.objects.create(
                user_id = request.user.id,
                product_id = request.POST.get('product_id'),
                quantity = request.POST.get('quantity') if request.POST.get('quantity') else 1,
                total = int(product.selling_price) * int(request.POST.get('quantity')) if request.POST.get('quantity') else product.selling_price,
            )
            messages.success(request,"Added to Cart")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('404')
    return redirect('login')

def AddAddress(request):
    if is_loggin(request):
        if is_method_post(request):

            address = UserAddress.objects.create(
                user_id = request.user.id,
                house_no = request.POST.get('house_no'),
                address_line_1 = request.POST.get('address_line_1'),
                address_line_2 = request.POST.get('address_line_2'),
                city = request.POST.get('city'),
                pin_code = request.POST.get('pin_code'),
                phone_number = request.POST.get('phone_number'),
                landmark = request.POST.get('landmark'),
            )
            messages.success(request,"Added")
            return redirect('addresses')
        return render(request,"add/address.html")
    return redirect('login')

def AddReview(request):
    if is_loggin(request):
        if is_method_post(request):

            review = Reviews.objects.create(
                user_id = request.user.id,
                nickname = request.POST.get('nickname'),
                reason = request.POST.get('reason'),
                comments = request.POST.get('comments'),
                rating = request.POST.get('rating'),
                date_time = request.POST.get('date_time'),
                product_id = request.POST.get('product_id'),
                is_read = False,
            )
            review.save()
            messages.success(request,"review added")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('500')
    return redirect('login')

def AddUser(request):
    if is_method_post(request):
        if Users.objects.all().first():
            user = User.objects.create_user(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
            )
        else:
            user = User.objects.create_superuser(
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
            )
        user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request,"Account Created")
        return redirect('login')
    return render(request,"authentication/signup.html")

def AddShopByCategoryProducts(request):
    if is_admin(request):
        if is_method_post(request):

            shop_by_category = ShopByCategory.objects.create(
                product_id = request.POST.get('product'), 
            )
            shop_by_category.save()
            messages.success(request,"✔️")
            return redirect(request.META.get("HTTP_REFERER"))
        return render(request,'add/shop_by_category')
    return redirect('404')

def OrderProduct(request):
    if is_loggin(request):

        if is_method_post(request):
            try:
                order = Orders.objects.create(
                    user_id = request.user.id,
                    address_id = request.POST.get('address'),
                    products = request.POST.get('products'),
                    total_price = request.POST.get('total_price'),
                    discount = request.POST.get('discount'),
                    discounted_price = request.POST.get('discounted_price'),
                    date_time = request.POST.get('date_time'),
                    is_completed = False
                )
                cart = Cart.objects.filter(user = request.user.id)
                cart.delete()
                order.save()
                messages.success(request,"Order Placed")
                return redirect('orders')
            except Exception as e:
                print(e)
                messages.error(request,"Error")
                return redirect(request.META.get("HTTP_REFERER"))
        return redirect('404')
    return redirect('login')

def Checkout(request):
    if is_loggin(request):
        cart = Cart.objects.filter(user = request.user.id)
        total = 0
        for item in cart:
            total = total + int(item.total)
        if is_method_post(request):
            products = []
            for item in cart:
                products.append(item.product.id)
            address = UserAddress.objects.create(
                user_id = request.user.id,
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
                company_name = request.POST.get('company_name'),
                address = request.POST.get('address'),
                city = request.POST.get('city'),
                state = request.POST.get('state'),
                order_notes = request.POST.get('order_notes'),
                country = request.POST.get('country'),
                pin_code = request.POST.get('pin_code'),
                phone_number = request.POST.get('phone_number'),
            )
            address.save()
            order = Orders.objects.create(
                user_id = request.user.id,
                address_id = address.id,
                products = products,
                total_price = request.POST.get('total_price'),
                date_time = request.POST.get('date_time'),
                is_completed = False,
            )
            order.save()
            messages.success(request,"order placed")
            return redirect('orders')
        return render(request,"checkout/checkout.html",{"cart_total":total})

def ContactForm(request):
    if is_method_post(request):

        contact = Contact.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            message = request.POST.get('message'),
            subject = request.POST.get('subject'),
            date_time = request.POST.get('date_time'),
            is_read = False,
        )
        contact.save()
        messages.success(request,"Sent ✔️")
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('404')

def Newsletter(request):
    if is_method_post(request):
        existing_newsletter = Newsletters.objects.filter(email = request.POST.get('email'))
        if existing_newsletter.exists():
            messages.success(request,"Already Signed Up")
            return redirect('homepage')
        newsletter = Newsletters.objects.create(
            email = request.POST.get('email'),
            date_time = request.POST.get('date_time'),
            is_approved = False,
        )
        newsletter.save()
        messages.success(request,"Signed Up")
        return redirect('homepage')

def AddBlog(request):
    if is_admin(request):
        if is_method_post(request):

            blog = Blogs.objects.create(
                user_id = request.user.id,
                publish_date = request.POST.get('publish_date'),
                title = request.POST.get('title'),
                description = request.POST.get('description'),
                is_published = request.POST.get('is_published') if request.POST.get('is_published') else True,
            )

            messages.success(request,"Added")
            return redirect('all-blogs')
        return render(request,"add/blog.html")
    return redirect('404')

def AddBlogComment(request):
    if is_loggin(request):
        if is_method_post(request):

            comment = BlogComments.objects.create(
                user_id = request.user.id,
                blog_id = request.POST.get('blog'),
                name = request.POST.get('name'),
                email = request.POST.get('email'),
                comment = request.POST.get('comment'),
                tags = request.POST.get('tags'),
                is_approved = request.POST.get('is_approved'),
            )
            messages.success(request,"comment added")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('500')
    return redirect('login')


# ============== Edit ========================= #

def EditCompany(request):
    if is_admin(request):
        company = Company.objects.all().first()
        if is_method_post(request):
            form = CompanyForm(request.POST,request.FILES,instance=company)
            if form.is_valid():
                form.save()
                messages.success(request,"updated")
                return redirect(request.META.get('HTTP_REFERER'))
            print(form.errors)
            return redirect('500')
        return render(request,"edit/company.html",{"company":company})
    return redirect('404')

def EditCategory(request,category_id):
    if is_admin(request):
        
        category = ProductCategory.objects.filter(id = category_id).first()
        if is_method_post(request):
            form = CategoryForm(request.POST,request.FILES,instance=category)
            if form.is_valid():
                form.save()
                messages.success(request,"updated")
                return redirect('all-categories')
            # category.update(
            #     name = request.POST.get('category_name')
            # )
            print(form.errors)
            messages.error(request,"something went wrong")
            return redirect('all-categories')
    return redirect('404')

def EditProduct(request,product_id):
    if is_admin(request):
        form1 = ProductForm()
        form2 = ImagesForm()
        product = Products.objects.filter(id = product_id).first()
        images_existing = Images.objects.filter(product = product_id)
        if is_method_post(request):
            form1 = ProductForm(request.POST,instance=product)
            if form1.is_valid():
                form1.save(commit=False)
            images = request.FILES.getlist('images')
            for image in images_existing:
                image_instance = Images.objects.filter(id = image.id).first()
                for img in images:
                    form2 = ImagesForm({"image":img},instance=image_instance)
                    if form2.is_valid():
                        form2.save()
            
            form1.save()
            return redirect('all-products')
        return render(request,'edit/product.html',{"product":product,"images":images_existing})
    return redirect('404')

def EditBanner(request,banner_id):
    if is_admin(request):
        banner = Banner.objects.filter(id = banner_id).first()
        if is_method_post(request):
            form = BannerForm(request.POST,request.FILES,instance=banner)
            if form.is_valid():
                form.save()
                messages.success(request,"✔️")
                return redirect(request.META.get('HTTP_REFERER'))
        return render(request,"edit/banner.html",{"banner":banner})
    return redirect('404')

def UpdateCartQunatity(request):
    if is_loggin(request):
        if is_method_post(request):

            cart_item = Cart.objects.filter(id = request.POST.get('cart_id'))
            cart_item.update(
                quantity = request.POST.get('qunatity')
            )
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('404')
    return redirect('login')

def UpdateAddress(request,address_id):
    if is_loggin(request):
        address = UserAddress.objects.filter(id = address_id)
        if is_method_post(request):

            address = address.update(
                house_no = request.POST.get('house_no'),
                address_line_1 = request.POST.get('address_line_1'),
                address_line_2 = request.POST.get('address_line_2'),
                city = request.POST.get('city'),
                pin_code = request.POST.get('pin_code'),
                phone_number = request.POST.get('phone_number'),
                landmark = request.POST.get('landmark'),
            )
            messages.success(request,"updated")
            return redirect(request.META.get('HTTP_REFERER'))
        return render(request,"address.html")
    return redirect('login')

def CompleteOrder(request):

    if is_admin(request):
        if is_method_post(request):
            order = Orders.objects.filter(id = request.POST.get('order_id'))
            order.update(
                is_completed = True
            )
            return redirect('admin-orders')
        return redirect('404')
    return redirect('404')

def ReadView(request):
    if is_admin(request):
        if is_method_post(request):
            review = Reviews.objects.filter(id = request.POST.get('review_id'))
            review.update(
                is_read = True
            )
            messages.success(request,"✔️")
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('500')

def ApproveNewsletter(request):
    if is_admin(request):
        if is_method_post(request):
            newsletter = Newsletters.objects.filter(id = request.POST.get('newsletter_id'))
            newsletter.update(
                is_approved = True
            )
            messages.success(request,"approved")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('404')
    return redirect('404')

def AproveContactForm(request):
    if is_admin(request):
        if is_method_post(request):

            contact = Contact.objects.filter(id = request.POST.get("contact_id"))
            contact.update(
                is_read = True,
            )
            messages.success(request,"✔️")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('500')
    return redirect('500')

def EditBlog(request,blog_id):
    if is_admin(request):
        blog = Blogs.objects.filter(id = blog_id)
        if is_method_post(request):
            blog.update(
                publish_date = request.POST.get('publish_date'),
                title = request.POST.get('title'),
                description = request.POST.get('description'),
                is_published = request.POST.get('is_published') if request.POST.get('is_published') else True,
            )

            messages.success(request,"Added")
            return redirect(request.META.get('HTTP_REFERER'))
        return render(request,"edit/blog.html",{"blog":blog.first()})
    return redirect('404')


# ============= Delete ====================== #

def DeleteCategory(request,category_id):
    if is_admin(request):
        if is_method_post(request):

            category = ProductCategory.objects.filter(id = category_id)
            category.delete()

            return redirect('all-categories')
    return redirect('404')

def DeleteProduct(request,product_id):
    if is_admin(request):
        if is_method_post(request):

            product = Products.objects.filter(id = product_id)
            product.delete()
            images = Images.objects.filter(product = product_id)
            images.delete()

            if images:
                for image in images:
                    if os.path.exists(image.image):
                        os.remove(image.image)
            return redirect('all-products')
    return redirect('404')

def DeleteBanner(request,banner_id):

    if is_admin(request):
        if is_method_post(request):
            banner = Banner.objects.filter(id = banner_id)
            banner.delete()
            messages.success(request,"deleted")
            return redirect('all-banners')
        return redirect('404')
    return redirect('404') 

def RemoveFromCart(request):
    if is_loggin(request):
        if is_method_post(request):
            cart_item = Cart.objects.filter(user = request.user.id).filter(product = request.POST.get('product_id'))
            cart_item.delete()
            messages.success(request,'Item Removed')
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('404')
    return redirect('login')

def DeleteAddress(request,address_id):
    if is_loggin(request):
        if is_method_post(request):
            address = UserAddress.objects.filter(id = address_id)
            address.delete()
            messages.success(request,"address removed")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('404')
    return redirect('login')

def DeleteBlog(request,blog_id):
    if is_admin(request):
        if is_method_post(request):
            blog = Blogs.objects.filter(id = blog_id)
            blog.delete()
            messages.success(request,"deleted")
            return render("all-blogs")
        return redirect('500')
    return redirect('400')

def DeleteBlogComment(request,comment_id):
    if is_loggin(request):
        if is_method_post(request):
            blog_comment = BlogComments.objects.filter(id =comment_id)
            blog_comment.delete()
            messages.success(request,"deleted")
            return render(request.META.get('HTTP_REFERER'))
        return redirect('500')
    return redirect('login')


# ============ Authentication ============= #
def UserLogin(request):
    if is_method_post(request):
        user = authenticate(username = request.POST.get('email'),password= request.POST.get('password'))
        if user:
            messages.success(request,'logged in')
            login(request,user)
            if user.is_superuser:
                return redirect('dashboard')
            return redirect('homepage')
        messages.error(request,"Incorrect email or password")
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'authentication/login.html')
     

def UserLogout(request):
    if is_loggin(request):
        if is_method_post(request):
            logout(request)
            messages.success(request,"logged out")
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('404')
    return redirect('login')
        



# ============= End User ================== #