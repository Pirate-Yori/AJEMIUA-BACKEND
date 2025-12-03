git clone <repo>
cd <repo>

python3 -m venv .env
.env/bin/activate

pip install -r requirements.txt

cd src
python manage.py migrate
python manage.py createsuperuser  /creer un superutilisateur (c'est lui qui a tout les droits sur l'app)

python manage.py runserver

NB : j'utilise SQlite
