pip install -r requirements.txt
python manage.py migrate
python manage.py seed_games
python manage.py sync_steam_prices --region us
python manage.py runserver
