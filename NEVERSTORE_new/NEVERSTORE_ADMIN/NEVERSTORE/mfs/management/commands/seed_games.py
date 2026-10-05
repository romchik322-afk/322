from datetime import date
from django.core.management.base import BaseCommand
from mfs.models import Game


# Каталог для стартового наповнення. Ціни є резервними: команда sync_steam_prices
# оновлює їх із Steam Store для регіону US.
GAMES = [
    (730, "Counter-Strike 2", "Безкоштовний змагальний шутер від Valve на рушії Source 2.", 0, 0, "Шутер / FPS", "Valve", "Valve", date(2012, 8, 21), True, False, False, True),
    (570, "Dota 2", "Глибока MOBA зі сотнями героїв, командною грою та постійними оновленнями.", 0, 0, "MOBA / Стратегія", "Valve", "Valve", date(2013, 7, 9), True, False, False, True),
    (1172470, "Apex Legends", "Швидкий hero-shooter і battle royale з унікальними легендами.", 0, 0, "Battle Royale / FPS", "Respawn Entertainment", "Electronic Arts", date(2020, 11, 4), True, False, False, True),
    (578080, "PUBG: BATTLEGROUNDS", "Один із найвідоміших battle royale: висаджуйся, збирай спорядження та виживай.", 0, 0, "Battle Royale / Шутер", "PUBG Studios", "KRAFTON", date(2017, 12, 21), True, False, False, True),
    (230410, "Warframe", "Космічний кооперативний екшен із сотнями місій, персонажів і зброї.", 0, 0, "Екшен / RPG / Кооп", "Digital Extremes", "Digital Extremes", date(2013, 3, 25), True, False, False, True),
    (1091500, "Cyberpunk 2077", "Сюжетна RPG у Найт-Сіті з відкритим світом, кібернетикою та нелінійними квестами.", 59.99, 59.99, "RPG / Відкритий світ", "CD PROJEKT RED", "CD PROJEKT RED", date(2020, 12, 9), True, True, False, False),
    (1245620, "ELDEN RING", "Масштабна action/RPG від FromSoftware з дослідженням Межизем'я та складними босами.", 59.99, 59.99, "Action RPG / Відкритий світ", "FromSoftware", "FromSoftware / Bandai Namco", date(2022, 2, 24), True, True, False, False),
    (292030, "The Witcher 3: Wild Hunt", "Велика рольова пригода Ґеральта з Рівії у відкритому світі.", 39.99, 39.99, "RPG / Відкритий світ", "CD PROJEKT RED", "CD PROJEKT RED", date(2015, 5, 18), True, True, False, False),
    (1174180, "Red Dead Redemption 2", "Епічна історія Артура Моргана та банди Ван дер Лінде в Америці 1899 року.", 59.99, 59.99, "Екшен / Пригода / Відкритий світ", "Rockstar Games", "Rockstar Games", date(2019, 12, 5), True, True, False, False),
    (1086940, "Baldur's Gate 3", "Рольова пригода у світі D&D, де рішення гравця змінюють історію.", 59.99, 59.99, "RPG / Стратегія / Пригода", "Larian Studios", "Larian Studios", date(2023, 8, 3), True, True, False, False),
    (3240220, "Grand Theft Auto V Enhanced", "Лос-Сантос з покращеною графікою та GTA Online.", 29.99, 29.99, "Екшен / Відкритий світ", "Rockstar North", "Rockstar Games", date(2025, 3, 4), True, True, False, False),
    (367520, "Hollow Knight", "Мальовниче метроідванія про дослідження занепалого підземного королівства.", 14.99, 14.99, "Metroidvania / Інді", "Team Cherry", "Team Cherry", date(2017, 2, 24), False, False, True, False),
    (413150, "Stardew Valley", "Затишна інді-гра про ферму, дружбу, дослідження та життя у долині.", 14.99, 14.99, "Симулятор / RPG / Інді", "ConcernedApe", "ConcernedApe", date(2016, 2, 26), False, False, True, False),
    (1240440, "Halo Infinite", "Науково-фантастичний шутер: безкоштовний багатокористувацький режим і кампанія.", 0, 0, "FPS / Sci-Fi / Multiplayer", "Halo Studios", "Xbox Game Studios", date(2021, 11, 15), False, False, False, True),
    (1151640, "Horizon Zero Dawn Complete Edition", "Пригода Елой у світі, де руїни людської цивілізації захопили механічні істоти.", 49.99, 49.99, "Action RPG / Відкритий світ", "Guerrilla", "PlayStation Publishing LLC", date(2020, 8, 7), True, True, False, False),
    (990080, "Hogwarts Legacy", "Відкритий світ у чарівному всесвіті Hogwarts Legacy з дослідженням замку та околиць.", 59.99, 59.99, "RPG / Пригода", "Avalanche Software", "Warner Bros. Games", date(2023, 2, 10), True, True, False, False),
    (2358720, "Black Myth: Wukong", "Динамічна action/RPG, натхненна китайською міфологією та легендою про Короля Мавп.", 59.99, 59.99, "Action RPG", "Game Science", "Game Science", date(2024, 8, 20), True, True, False, False),
    (553850, "HELLDIVERS 2", "Вибуховий кооперативний шутер, де команда бореться за свободу галактики.", 39.99, 39.99, "Шутер / Кооп", "Arrowhead Game Studios", "PlayStation Publishing LLC", date(2024, 2, 8), True, True, False, False),
    (1145360, "Hades", "Стильний roguelike-екшен про спробу втекти з підземного світу.", 24.99, 24.99, "Roguelike / Action RPG", "Supergiant Games", "Supergiant Games", date(2020, 9, 17), False, False, True, False),
    (1145350, "Hades II", "Продовження динамічної roguelike-серії Supergiant Games.", 29.99, 29.99, "Roguelike / Action RPG", "Supergiant Games", "Supergiant Games", date(2025, 9, 25), True, False, True, False),
    (588650, "Dead Cells", "Швидкий roguelite метроідванія з безліччю зброї, маршрутів і босів.", 24.99, 24.99, "Roguelite / Metroidvania", "Motion Twin", "Motion Twin", date(2018, 8, 6), False, False, True, False),
    (105600, "Terraria", "Пісочниця-пригода з будівництвом, дослідженням, крафтом і битвами.", 9.99, 9.99, "Sandbox / Пригода / Інді", "Re-Logic", "Re-Logic", date(2011, 5, 16), True, False, True, False),
    (892970, "Valheim", "Виживання та дослідження міфічного світу в кооперативі до 10 гравців.", 19.99, 19.99, "Виживання / Кооп / Інді", "Iron Gate AB", "Coffee Stain Publishing", date(2021, 2, 2), True, False, True, False),
    (252490, "Rust", "Жорстке онлайн-виживання: ресурси, будівництво, рейди та боротьба з іншими гравцями.", 39.99, 39.99, "Виживання / Multiplayer", "Facepunch Studios", "Facepunch Studios", date(2018, 2, 8), True, True, False, False),
    (1623730, "Palworld", "Виживання, будівництво, дослідження та істоти, яких можна приручати.", 29.99, 29.99, "Survival / Open World", "Pocketpair", "Pocketpair", date(2024, 1, 19), True, False, False, False),
    (1966720, "Lethal Company", "Кооперативний хорор про збір брухту на покинутих супутниках.", 9.99, 9.99, "Хорор / Кооп / Інді", "Zeekerss", "Zeekerss", date(2023, 10, 9), True, False, True, False),
    (739630, "Phasmophobia", "Кооперативний психологічний хорор про полювання на привидів.", 19.99, 19.99, "Хорор / Кооп", "Kinetic Games", "Kinetic Games", date(2020, 9, 18), True, False, True, False),
    (548430, "Deep Rock Galactic", "Кооперативний FPS про космічних шахтарів, печери та орди прибульців.", 29.99, 29.99, "FPS / Кооп", "Ghost Ship Games", "Coffee Stain Publishing", date(2020, 5, 13), True, False, True, False),
    (550, "Left 4 Dead 2", "Класичний кооперативний шутер Valve про виживання серед орд заражених.", 9.99, 9.99, "FPS / Кооп", "Valve", "Valve", date(2009, 11, 17), True, False, False, False),
    (440, "Team Fortress 2", "Безкоштовний командний шутер із класами, гумором і величезною кількістю косметики.", 0, 0, "FPS / Multiplayer", "Valve", "Valve", date(2007, 10, 10), True, False, False, True),
    (108600, "Project Zomboid", "Глибокий симулятор виживання під час зомбі-апокаліпсису.", 19.99, 19.99, "Survival / RPG / Інді", "The Indie Stone", "The Indie Stone", date(2013, 11, 8), False, False, True, False),
    (322330, "Don't Starve Together", "Темна кооперативна survival-пригода з дивними істотами та безліччю механік.", 14.99, 14.99, "Survival / Кооп / Інді", "Klei Entertainment", "Klei Entertainment", date(2016, 4, 21), False, False, True, False),
    (304050, "Trove", "Безкоштовна кубічна MMO з підземеллями, класами, будівництвом і пригодами.", 0, 0, "MMO / RPG / Інді", "Trion Worlds", "Gamigo US Inc.", date(2015, 7, 9), False, False, True, True),
    (1174180, "Red Dead Redemption 2", "Епічна історія Артура Моргана у деталізованому світі Дикого Заходу.", 59.99, 59.99, "Екшен / Пригода", "Rockstar Games", "Rockstar Games", date(2019, 12, 5), True, True, False, False),
]


def game_dict(item):
    app_id, title, description, price, old_price, genre, developer, publisher, release_date, popular, aaa, indie, free = item
    return {
        "steam_app_id": app_id,
        "title": title,
        "description": description,
        "price": price,
        "old_price": old_price,
        "genre": genre,
        "developer": developer,
        "publisher": publisher,
        "release_date": release_date,
        "is_popular": popular,
        "is_aaa": aaa,
        "is_indie": indie,
        "is_free_to_play": free,
        "image_url": f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg",
        "price_currency": "USD",
    }


class Command(BaseCommand):
    help = "Наповнює NEVERSTORE каталогом популярних ігор"

    def handle(self, *args, **options):
        seen = set()
        updated_count = 0
        for item in GAMES:
            data = game_dict(item)
            app_id = data["steam_app_id"]
            if app_id in seen:
                continue
            seen.add(app_id)
            Game.objects.update_or_create(steam_app_id=app_id, defaults=data)
            updated_count += 1
        self.stdout.write(self.style.SUCCESS(f"Додано/оновлено ігор: {updated_count}"))
