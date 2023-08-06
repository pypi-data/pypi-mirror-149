django-clients_ds
==========

django-clients_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "clients" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'clients',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load clients_tags %}
{% make_clients %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "clients": ["amc", "cmc", "khmc", "pnuh", "sev", "smc", "snuh"]
}
```
