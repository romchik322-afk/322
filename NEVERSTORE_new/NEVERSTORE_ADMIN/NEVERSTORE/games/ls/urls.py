from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from mfs import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("login/", views.login_view, name="login"),
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/game/<int:game_id>/edit/", views.admin_edit_game, name="admin_edit_game"),
    path("admin-dashboard/game/<int:game_id>/delete/", views.admin_delete_game, name="admin_delete_game"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("profile/", views.profile, name="profile"),
    path("library/", views.library, name="library"),

    path("game/<int:game_id>/", views.game_detail, name="game"),
    path("game/<int:game_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("game/<int:game_id>/rate/", views.rate_game, name="rate_game"),

    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:game_id>/", views.add_to_cart, name="add_to_cart"),

    path("buy/<int:game_id>/", views.buy_game, name="buy_game"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
