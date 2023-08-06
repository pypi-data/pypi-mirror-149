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

* 팀멤버는 최대 6인까지 가능하며 1인인 경우는 템플릿이 어울리지 않을수 있다.
* 템플릿을 추가할때 section 명은 team으로 수정해야 북마크링크가 걸릴수 있다.

* context example
```python
context = {
    "theme": "bethany_ds",
    "team": {
        "title": "닥터",
        "subtitle": "닥터",
        "type": "career",  # career or desc
        "members": [
            {
                "name": "김형진",
                "title": "대표원장",
                "desc": "Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut",
                "career": [
                    "구강악안면외과 국가전문의",
                    "삼성서울병원 구강외과 전공",
                    "삼성서울병원 치과진료부 외래교수",
                    "대한구강악안면성형외과학회 인정의",
                    "원광대학교 치과대학 졸업",
                    "EAO(유럽임플란트학회) 정회원",
                    "대한치과보철학회 정회원",
                    "삼성서울병원 교정과 Residency course",
                    "Osstem AIC 임상지도의"
                ],
                "certs": [
                    "치과의사전문의자격증",
                    "구강악안면성형외과자격증",
                    "오스템지도의",
                    "삼성서울병원외래교수"
                ],
                "social": {
                    "twitter": "",
                    "facebook": "",
                    "instagram": "https://blog.naver.com/mylife2879",
                    "linkedin": "https://blog.naver.com/mylife2879",
                },
            },
            {
                "name": "설정은",
                "title": "부원장",
                "desc": "Magni qui quod omnis unde et eos fuga et exercitationem. Odio veritatis perspiciatis quaerat qui aut aut aut",
                "career": [
                    "카톨릭대학교 치아교정학 전공",
                    "삼성서울병원 치과진료부 외래교수",
                    "부산대학교 치의학과 졸업",
                    "대한 치아교정학회 정회원",
                    "대한 심미치과학회 정회원",
                    "인비절라인(INVISALIGN) 인증의",
                    "인코그니토(INCOGNITO) 인증의"
                ],
                "certs": [
                    "치과의사전문의자격증",
                    "구강악안면성형외과자격증",
                    "오스템지도의",
                    "삼성서울병원외래교수"
                ],
                "social": {
                    "twitter": "https://blog.naver.com/mylife2879",
                    "facebook": "https://blog.naver.com/mylife2879",
                    "instagram": "",
                    "linkedin": "",
                },
            }
        ]
    }
}
```
