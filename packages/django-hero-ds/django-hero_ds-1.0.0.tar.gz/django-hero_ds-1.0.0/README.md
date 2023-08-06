django-hero_ds
==========

django-hero_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "hero" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'hero',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load hero_tags %}
{% make_hero %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "hero": {
        "bg": "bg1",
        "title": "Say Tell Speak Talk",
        "slogan": "Global connection starts with improving your speaking skills<br>Let’s get to talking!",
        "btn": {"title": "Classes", "link": "#classes"}
    }
}
```
