django-counts_ds
==========

django-counts_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "counts" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'counts',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load counts_tags %}
{% make_counts %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "counts": [
            ["학생", 17],
            ["클래스", 4],
            ["이벤트", 3],
            ["교사", 1]
        ]
}
```

* Required vendor - purecounter