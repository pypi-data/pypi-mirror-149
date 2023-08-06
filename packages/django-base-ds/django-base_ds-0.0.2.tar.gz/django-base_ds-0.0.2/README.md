django-base_ds
==========

django-base_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "base" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'base',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load base_tags %}

{% make_seo %}
{% make_vendor_css %}
{% make_vendor_js %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "seo": {
        "company_name": "MyEnglish",
        "url": "myenglishkr.com",
        "small_title": "1:1 Speaking Practice",
        "desc": "강남구 서초동 교대 반포 법조타운 위치 내인생치과의 홈페이지, 삼성서울병원 구강외과 전문의 진료",
        "keywords": "내인생치과, 반포대로치과, 교대교정치과, 반포치과, 서초치과, 서초동치과, 교대역치과 "
    },
}
```
