from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from datetime import date
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import RegisterForm, LoginForm, AdminLoginForm, GameAdminForm
from .models import Game, Profile, Library, Favorite, Cart, GameRating


def home(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    category = request.GET.get("category", "").strip()

    games_qs = Game.objects.annotate(avg_rating=Avg("ratings__value"), rating_count=Count("ratings"))
    if query:
        games_qs = games_qs.filter(title__icontains=query)
    if genre:
        games_qs = games_qs.filter(genre__icontains=genre)
    if category == "aaa":
        games_qs = games_qs.filter(is_aaa=True)
    elif category == "indie":
        games_qs = games_qs.filter(is_indie=True)
    elif category == "free":
        games_qs = games_qs.filter(is_free_to_play=True)

    games = games_qs.order_by("-is_popular", "-created_at")[:24]
    popular_games = Game.objects.annotate(avg_rating=Avg("ratings__value"), rating_count=Count("ratings")).filter(is_popular=True).order_by("-created_at")[:8]
    genres = Game.objects.exclude(genre="").values_list("genre", flat=True).distinct()
    catalog_games = list(Game.objects.order_by("id"))
    daily_game = catalog_games[date.today().toordinal() % len(catalog_games)] if catalog_games else None
    free_count = Game.objects.filter(is_free_to_play=True).count()
    aaa_count = Game.objects.filter(is_aaa=True).count()
    indie_count = Game.objects.filter(is_indie=True).count()

    return render(request, "home.html", {
        "games": games,
        "popular_games": popular_games,
        "genres": genres,
        "query": query,
        "selected_genre": genre,
        "category": category,
        "daily_game": daily_game,
        "catalog_count": len(catalog_games),
        "free_count": free_count,
        "aaa_count": aaa_count,
        "indie_count": indie_count,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            Cart.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("home")
            form.add_error(None, "Невірний логін або пароль")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})



def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None and user.is_staff:
                login(request, user)
                return redirect("admin_dashboard")
            form.add_error(None, "Невірний логін, пароль або немає прав адміністратора")
    else:
        form = AdminLoginForm()
    return render(request, "admin_login.html", {"form": form})


def staff_required(view_func):
    return login_required(user_passes_test(lambda user: user.is_staff, login_url="admin_login")(view_func))


@staff_required
def admin_dashboard(request):
    games = Game.objects.order_by("-created_at")

    if request.method == "POST":
        form = GameAdminForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            messages.success(request, f"Гру «{game.title}» успішно додано до магазину.")
            return redirect("admin_dashboard")
        messages.error(request, "Гру не додано. Перевірте помилки у формі нижче.")
    else:
        form = GameAdminForm()

    return render(request, "admin_dashboard.html", {
        "form": form,
        "games": games,
    })


@staff_required
def admin_edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        form = GameAdminForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            game = form.save()
            messages.success(request, f"Гру «{game.title}» оновлено.")
            return redirect("admin_dashboard")
        messages.error(request, "Гру не оновлено. Перевірте помилки у формі.")
    else:
        form = GameAdminForm(instance=game)

    return render(request, "admin_dashboard.html", {
        "form": form,
        "games": Game.objects.order_by("-created_at"),
        "editing_game": game,
    })


@staff_required
@require_POST
def admin_delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    title = game.title
    game.delete()
    messages.success(request, f"Гру «{title}» видалено.")
    return redirect("admin_dashboard")

def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    games_count = Library.objects.filter(user=request.user).count()
    favorites_count = Favorite.objects.filter(user=request.user).count()
    return render(request, "profile.html", {"profile": profile_obj, "games_count": games_count, "favorites_count": favorites_count})


def game_detail(request, game_id):
    game = get_object_or_404(Game.objects.annotate(avg_rating=Avg("ratings__value"), rating_count=Count("ratings")), id=game_id)
    owned = False
    favorite = False
    user_rating = None
    if request.user.is_authenticated:
        owned = Library.objects.filter(user=request.user, game=game).exists()
        favorite = Favorite.objects.filter(user=request.user, game=game).exists()
        user_rating = GameRating.objects.filter(user=request.user, game=game).values_list("value", flat=True).first()
    return render(request, "game.html", {"game": game, "owned": owned, "favorite": favorite, "user_rating": user_rating})


@login_required
def toggle_favorite(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)
    if not created:
        favorite.delete()
    return redirect("game", game_id=game_id)


@login_required
@require_POST
def rate_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    try:
        value = max(1, min(5, int(request.POST.get("rating", 0))))
    except (TypeError, ValueError):
        return redirect("game", game_id=game_id)
    GameRating.objects.update_or_create(user=request.user, game=game, defaults={"value": value})
    return redirect("game", game_id=game_id)


@login_required
def library(request):
    games = Game.objects.filter(library__user=request.user)
    return render(request, "library.html", {"games": games})


@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.games.add(game)
    return redirect("cart")


@login_required
def cart(request):
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart_obj})


@login_required
def buy_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    profile = Profile.objects.get(user=request.user)
    if Library.objects.filter(user=request.user, game=game).exists():
        return redirect("library")
    if profile.balance >= game.price:
        profile.balance -= game.price
        profile.save()
        Library.objects.create(user=request.user, game=game)
        cart = Cart.objects.get(user=request.user)
        cart.games.remove(game)
    return redirect("library")
