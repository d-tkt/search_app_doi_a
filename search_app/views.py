from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Favorite, CartItem
from .forms import ProductForm, SearchForm 
from django.core.paginator import Paginator 
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse

def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check)
def product_create(request): 
    if request.method == 'POST': 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_list') 
    else: 
        form = ProductForm() 
    return render(request, 'search/product_form.html', {'form': form}) 

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_favorite = False
    cart_quantity = 0  # カート内の数量を初期化

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
        # カート内の数量を取得
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
        if cart_item:
            cart_quantity = cart_item.quantity

    return render(request, 'search/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
        'cart_quantity': cart_quantity,  # カートの数量をコンテキストに追加
    })

@user_passes_test(superuser_check)
def product_update(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_detail', pk=product.pk) 
    else: 
        form = ProductForm(instance=product) 
    return render(request, 'search/product_form.html', {'form': form, 'product': product})

@user_passes_test(superuser_check)
def product_delete(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        product.delete() 
        return redirect('product_list') 
    return render(request, 'search/product_confirm_delete.html', {'product': product}) 

@user_passes_test(superuser_check)
def product_list(request): 
    products = Product.objects.all() 
    return render(request, 'search/product_list.html', {'products': products}) 

def search_view(request):
    # セッションから検索条件を取得または初期化
    search_params = request.session.get('search_params', {
        'query': '',
        'category': '',
        'min_price': '',
        'max_price': '',
        'sort': 'name'
    })

    # 新しい検索条件の適用
    if request.GET:
        search_params = {
            'query': request.GET.get('query', ''),
            'category': request.GET.get('category', ''),
            'min_price': request.GET.get('min_price', ''),
            'max_price': request.GET.get('max_price', ''),
            'sort': request.GET.get('sort', 'name')
        }

    # セッションの更新
    request.session['search_params'] = search_params

    # 検索条件の適用
    results = Product.objects.all()
    print(f"初期の製品数: {results.count()}")

    if search_params['query']:
        results = results.filter(name__icontains=search_params['query'])
        print(f"クエリ適用後の製品数: {results.count()}")

    if search_params['category'] and search_params['category'] != 'すべて':
        results = results.filter(category__name=search_params['category'])
        print(f"カテゴリ適用後の製品数: {results.count()}")

    if search_params['min_price']:
        results = results.filter(price__gte=float(search_params['min_price']))
        print(f"最小価格適用後の製品数: {results.count()}")

    if search_params['max_price']:
        results = results.filter(price__lte=float(search_params['max_price']))
        print(f"最大価格適用後の製品数: {results.count()}")

    # 並び替え
    if search_params['sort'] == 'price_asc':
        results = results.order_by('price')
    elif search_params['sort'] == 'price_desc':
        results = results.order_by('-price')
    else:
        results = results.order_by('name')

    # ページネーション
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # フォームの初期値を設定
    form = SearchForm(initial=search_params)

    context = {
        'form': form,
        'page_obj': page_obj,
        'search_params': search_params,
        'categories': Category.objects.all(),
    }

    return render(request, 'search/search.html', context)

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
    
    # リファラを取得してリダイレクト
    referer = request.META.get('HTTP_REFERER', 'favorite_list')  # デフォルトはお気に入りリスト
    return redirect(referer)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # リファラを取得してリダイレクト
    referer = request.META.get('HTTP_REFERER', 'cart_list')  # デフォルトはカートリスト
    return redirect(referer)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'search/favorite_list.html', {'favorites': favorites})

@login_required
def cart_list(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    return render(request, 'search/cart_list.html', context)

@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
    cart_item.delete()
    return redirect('cart_list')

@login_required
def remove_one_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # 数量が1の場合はアイテムを削除
    return redirect('cart_list')
