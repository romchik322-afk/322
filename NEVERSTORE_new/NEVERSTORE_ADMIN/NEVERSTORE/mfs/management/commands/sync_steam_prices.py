import json
import os
from datetime import datetime, timezone
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from mfs.models import Game


class Command(BaseCommand):
    help = "Оновлює ціни, обкладинки та базові дані ігор зі Steam Store API"

    def add_arguments(self, parser):
        parser.add_argument("--region", default=os.getenv("NEVERSTORE_REGION", "us"), help="Код регіону Steam, наприклад us або ua")

    def handle(self, *args, **options):
        region = options["region"].lower()
        games = Game.objects.exclude(steam_app_id__isnull=True)
        updated = 0

        for game in games:
            url = f"https://store.steampowered.com/api/appdetails?appids={game.steam_app_id}&cc={region}&l=uk"
            try:
                request = Request(url, headers={"User-Agent": "NEVERSTORE/1.0"})
                with urlopen(request, timeout=12) as response:
                    payload = json.load(response)
                data = payload.get(str(game.steam_app_id), {})
                if not data.get("success"):
                    continue
                info = data.get("data", {})
                price = info.get("price_overview")
                if price:
                    game.price = price["final"] / 100
                    game.old_price = price.get("initial", price["final"]) / 100
                    game.price_currency = price.get("currency", game.price_currency or "USD")
                elif info.get("is_free"):
                    game.price = 0
                    game.old_price = 0
                    game.price_currency = game.price_currency or "USD"
                if info.get("header_image"):
                    game.image_url = info["header_image"]
                if info.get("developers"):
                    game.developer = info["developers"][0]
                if info.get("publishers"):
                    game.publisher = info["publishers"][0]
                game.price_updated_at = datetime.now(timezone.utc)
                game.save(update_fields=["price", "old_price", "price_currency", "image_url", "developer", "publisher", "price_updated_at"])
                updated += 1
            except Exception as exc:
                self.stderr.write(f"{game.title}: {exc}")

        self.stdout.write(self.style.SUCCESS(f"Синхронізовано: {updated}; регіон Steam: {region.upper()}"))
