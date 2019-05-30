#Create virtualenv

    python3 -m pip install --user virtualenv
    python3 -m venv venv

#Activate env

    source venv/bin/activate


#Install requirements

    pip install -r requirements.txt
    
#Apply migrations

    python manage.py migrate
    
#Create superuser

    python manage.py createsuperuser
    
#Run app

    python manage.py runserver
    
