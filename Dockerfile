FROM python:3.6.5
MAINTAINER Dmitry Gamanenko
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 
RUN python manage.py migrate --noinput && python manage.py collectstatic --noinput 
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'letmein123')" | ./manage.py shell
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
