django-portfolio_ds
==========

django-portfolio_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "portfolio" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'portfolio',
    'base',
]
```

2. Run below command to create the portfolio models.::
```commandline
    python manage.py makemigrations portfolio
    python manage.py migrate
    python manage.py createsuperuser
```

3. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load portfolio_tags %}
{% make_portfolio %}
```

4. http://127.0.0.1:8000/admin 으로 접속하여 데이터베이스 자료를 입력한다.

5. media 파일을 찾을 수 있도록 프로젝트의 url.py에 다음을 추가한다.
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
    path('portfolio/', include('portfolio.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

* context example
```python
context = {
    "theme": "medilab_ds",
    'color': "default",
    "portfolio": {
        'title': "케이스",
        'subtitle': '주목할 만한 치과 케이스 모음',
    }
}
```

