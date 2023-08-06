django-cta_ds
==========

django-cta_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "cta" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'cta',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load cta_tags %}
{% make_cta %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "cta": {
            "title" : "카카오톡 상담",
            "desc" : "카카오톡을 통해 상담 및 예약 가능합니다.",
            "link" : "http://pf.kakao.com/_xexhxgxlV"
    }
}
```
