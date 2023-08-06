django-appointment_ds
==========

django-appointment_ds is a Django app to use for demiansoft.

Quick start
------------

1. Add "fav_stock" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'appointment',
]
```
    
2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load appointment_tags %}
{% make_appointment %}
```

3. post 메시지 처리를 위한 make_post_context 함수를 사용한다.
```python
from appointment.templatetags.appointment_tags import make_post_context

...

if request.method == "POST":
    context.update(make_post_context(request.POST, 'hj3415@gmail.com'))
    return render(request, f"home/home.html", context)
```

* context example
```python
context = {
        "color": "default",
        "theme": "medilab_ds",
        "naver": "https://booking.naver.com/booking/13/bizes/441781",
    }
```

* Required vendor - jquery

* contact 에 포함된 appointment 폼을 추출하는 경우 - 따로 appointment 섹션이 없기 때문에 css 파일과 html 파일의 contact 에서 php-email-form 파트를
 추출 하여 .contact 을 .appointment 로 .php-email-form 을 .email-form 으로 일괄 변환 한다.
