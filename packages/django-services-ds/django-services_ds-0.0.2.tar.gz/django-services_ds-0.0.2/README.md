django-services_ds
==========

django-services_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "services" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'services',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load services_tags %}
{% make_services %}
```

* bethany icon - bxl
* medilab icon - fa

* context example
```python
context = {
    "theme": "bethany_ds",
    "services": {
        "title": "서비스",
        "subtitle": "서브타이틀",
        "type": "icon",  # icon or image
        "items": [
            {
                "image_filename": "1.png",
                "icon": "fa-stethoscope",  # bxl-dribbble
                "title": "어려운 케이스 및 당일 사랑니 발치 수술이 가능합니다.",
                "desc": "대학병원으로 의뢰하는 다양한 고난이도의 사랑니를 20여년 경력의 구강외과 전문의가 발치합니다."
            },
            {
                "image_filename": "3.png",
                "icon": "fa-hospital",
                "title": "편리한 접근성으로 내원이 용이합니다.",
                "desc": "교대역 출구 1분 거리에 위치해 있어 찾기가 쉽고 대중교통 이용시 접근성이 편리합니다."
            },
            {
                "image_filename": "4.png",
                "icon": "fa-hand-sparkles",
                "title": "한차원 높은 소독시스템.",
                "desc": "핸드피스 전용 소독기와 모든 체어 및 대기실에 LED 공간 표면 살균기 가동 "
            }
        ]
    }
}
```
