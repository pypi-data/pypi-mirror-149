django-contact_ds
==========

django-contact_ds is a Django app to use for stockanalyser. For each question,
visitors can choose between a fixed number of answers.

Quick start
------------

1. Add "fav_stock" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'contact',
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
