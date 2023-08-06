django-whyus_ds
==========

django-whyus_ds is a Django app to use for demiansoft. 

Quick start
------------

1. Add "whyus" to your INSTALLED_APPS setting like this
```python
INSTALLED_APPS = [
    ...
    'whyus',
]
```

2. 코드를 넣고자 하는 위치에 다음을 추가 한다.
```html
{% load whyus_tags %}
{% make_whyus %}
```

* context example
```python
context = {
    "theme": "mentor_ds",
    "whyus" : {
            "major" : {
              "title" : "치과전문의 진료",
              "contents" : [
                "구강악안면외과와 교정과를 전공한 원장님들의 특화된 진료를 제공합니다."
              ],
              "link" : "#doctors"
            },
            "_comment_type" : "icon or image",
            "type" : "icon",

            "_comment_icon" : "https://boxicons.com/ [bx-group, bx-pulse, bx-buildings, bx-bed]",
            "minor" : [
              {
                "icon": "bx-buildings",
                "title": "상급병원과의 연계",
                "contents": "삼성서울병원과의 유기적인 협력관계로 신속한 연계가 가능합니다. (대표원장 현 삼성서울병원 외래교수 재직)"
              },
              {
                "icon": "bx-pulse",
                "title": "당일 사랑니발치",
                "contents": "치과용 CT를 이용한 정밀검사를 통해 수술이 필요한 사랑니도 발치가 가능합니다."
              },
              {
                "icon": "bx-bed",
                "title": "수면진정치료",
                "contents": "치과공포증으로 치료가 어려웠던 환자분들도 안전하고 편안하게 수면진정치료를 받으실 수 있습니다."
              }
            ]
        }
}
```
