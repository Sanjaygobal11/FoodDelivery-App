from django.shortcuts import render, redirect
from .models import Food, Order, Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse



def home(request):
    foods = Food.objects.all()
    return render(request, 'home.html', {'foods': foods})

@login_required
def order_food(request, food_id):
    food = Food.objects.get(id=food_id)

    if request.method == "POST":
        customer_name = request.POST['customer_name']
        quantity = int(request.POST['quantity'])

        total = food.price * quantity

        Order.objects.create(
            customer_name=customer_name,
            food=food,
            quantity=quantity,
            total_price=total
        )

        return redirect('/')

    return render(request, 'order.html', {'food': food})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'items': items})

@login_required
def add_to_cart(request, food_id):
    food = Food.objects.get(id=food_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/')

def category_foods(request, category):
    foods = Food.objects.filter(category=category)
    return render(request, 'category.html', {
        'foods': foods,
        'category': category
    })

def home(request):
    query = request.GET.get('q')

    if query:
        foods = Food.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )
    else:
        foods = Food.objects.all()

    return render(request, 'home.html', {'foods': foods})

@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    total = 0
    for item in items:
        total += item.food.price * item.quantity

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })

@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    total = 0
    for item in items:
        total += item.food.price * item.quantity

    if request.method == "POST":
        address = request.POST['address']
        phone = request.POST['phone']
        payment = request.POST['payment']

        for item in items:
            Order.objects.create(
                customer_name=request.user.username,
                food=item.food,
                quantity=item.quantity,
                total_price=item.food.price * item.quantity,
                address=address,
                phone=phone,
                payment_method=payment
            )

        items.delete()

        return render(request, 'success.html')

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(
        customer_name=request.user.username
    ).order_by('-id')

    return render(request, 'order_history.html', {
        'orders': orders
    })

def about(request):
    return render(request, 'about.html')

@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_foods = Food.objects.count()

    revenue = Order.objects.aggregate(
        Sum('total_price')
    )['total_price__sum']

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_foods': total_foods,
        'revenue': revenue or 0
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )


def food_api(request):
    foods = Food.objects.all()

    data = []
    for f in foods:
        data.append({
            "id": f.id,
            "name": f.name,
            "price": f.price,
            "image": f.image.url
        })

    return JsonResponse(data, safe=False)