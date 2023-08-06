django-team_ds
==========

django-team_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "team" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'team',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load team_tags %}
{% make_team %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "team" : {
        }
}
```
