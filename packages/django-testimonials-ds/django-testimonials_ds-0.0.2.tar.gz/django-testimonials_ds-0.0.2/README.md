django-testimonials_ds
==========

django-testimonials_ds is a Django app to use for demiansoft.

Quick start
------------

1. Add "testimonials" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'testimonials',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load testimonials_tags %}
{% make_testimonials %}
```

3. static/img/testimonials 폴더에 인물사진을 넣는다.

* context example
```python
context = {
    "theme": "mentor_ds",
    "testimonials": {
        "subtitle": "What are they saying",
        "stories": [
            {
          "photo": "testimonials-1",
          "name": "Hyungjin Kim",
          "job": "Dentist",
          "desc": "훌륭하고 친절한 선생님과 좋은 내용의 커리큘럼입니다."
        },
        {
          "photo": "testimonials-2",
          "name": "Jungeun Seol",
          "job": "CEO",
          "desc": "훌륭하고 친절한 선생님과 좋은 내용의 커리큘럼입니다."
        }
      ]
    }
}
```


* Required vendor - swiper

