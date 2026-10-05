from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to="games/", blank=True, null=True)
    image_url = models.URLField(blank=True, default="")
    steam_app_id = models.PositiveIntegerField(blank=True, null=True, unique=True)
    is_popular = models.BooleanField(default=False)
    is_indie = models.BooleanField(default=False)
    is_aaa = models.BooleanField(default=False)
    is_free_to_play = models.BooleanField(default=False)
    price_currency = models.CharField(max_length=8, default="USD")
    price_updated_at = models.DateTimeField(blank=True, null=True)
    developer = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round((1 - float(self.price / self.old_price)) * 100)
        return 0

    def __str__(self):
        return self.title


class Library(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "game")


class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ratings")
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, blank=True)

    def total(self):
        return sum(game.price for game in self.games.all())
