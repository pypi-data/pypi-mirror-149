django-appointment_ds
==========

django-fav_stock is a Django app to use for stockanalyser. For each question,
visitors can choose between a fixed number of answers.

contact에 포함된 폼의 경우는 따로 appointment 섹션이 없기 때문에 css파일과 html파일의 contact에서 php-email-form파트를
추출한여 .contact을 .appointment로 .php-email-form을 .email-form으로 일괄 변환한다.

Quick start
------------

1. Add "fav_stock" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'appointment',
    ]

2. Run below command to create the fav_stock models.::

    python manage.py makemigrations fav_stock
    python manage.py migrate
    python manage.py createsuperuser

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a fav_stock (you'll need the Admin app enabled).

4. Add the namespace in urlpattern like this::

    urlpatterns = [
    ...
      path('fav/', include('fav_stock.urls', namespace='fav_stock')),
    ]

5. Usage in the template::

    {% load fav_stock_custom_tags %}
    ...
    {% add_n_edit_fav code="005930" %}
    {% del_fav code="005930" %}

6. If you want to see appropriate html render, please use bootstrap 5.
