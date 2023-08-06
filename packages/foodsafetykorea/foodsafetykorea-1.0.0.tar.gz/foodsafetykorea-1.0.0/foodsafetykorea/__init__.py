import requests
import fake_useragent
from urllib.parse import urlencode

from .models import *
from .utils import month, year, week_count

session = requests.Session()
user_agent = fake_useragent.UserAgent(verify_ssl=False).random

def replace_user_agent(new_user_agent):
    global user_agent
    user_agent = new_user_agent
    return None

def refresh_user_agent():
    return replace_user_agent(fake_useragent.UserAgent(verify_ssl=False).random)

def replace_session(new_session):
    global session
    session = new_session
    return None

def refresh_session():
    return replace_session(requests.Session())

def select_school_meals(school, area = None):
    response = session.post(
        'https://foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolMeals_school.do',
        data=urlencode(
            dict(
                copyUrl='https://foodsafetykorea.go.kr:443/portal/sensuousmenu/schoolMealsDetail.do?',
                favorListCnt=0,
                month=month,
                select_year=year,
                select_month=month,
                region=area or '',
                search_keyword=school,
                week=week_count,
                year=year,
                select_week=week_count,
            )
        ),
        headers={
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    )

    mapping = response.json()
    return [Meals(**map) for map in mapping['list']]

def select_school_meals_info(map, /, area = None):
    response = session.post(
        'https://foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolMealsInfo.do',
        data=urlencode(
            dict(
                copyUrl='https://foodsafetykorea.go.kr:443/portal/sensuousmenu/schoolMealsDetail.do?',
                favorListCnt=0,
                schl_cd=map.schl_cd,
                select_year=year,
                select_month=month,
                search_keyword=map.schl_nm,
                month=month,
                type_cd='W',
                week=week_count,
                select_week=week_count,
                year=year,
                region=area or ''
            )
        ),
        headers={
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        },
    )

    json = response.json()

    return MealsInfo(**json['schoolMealsInfo'])

def select_week_year_list(selected):
    response = session.post(
        'https://foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolWeekYearList.do',
        data=urlencode(
            dict(schl_cd=selected.schl_cd),
        ),
        headers={
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        },
    )

    json = response.json()
    result = [WeekYearList(**value) for value in json['list']]

    return result

def select_school_week_meals_detail(selected, /):
    response = session.post(
        'https://foodsafetykorea.go.kr/portal/sensuousmenu/selectSchoolWeekMealsDetail.do',
        data=urlencode(
            dict(
                copyUrl='https://foodsafetykorea.go.kr:443/portal/sensuousmenu/schoolMealsDetail.do?',
                favorListCnt=0,
                schl_cd=selected.schl_cd,
                type_cd='W',
                year=selected.year,
                month=selected.month,
                week=selected.week,
                select_year=selected.year,
                select_month=selected.month,
                select_week=selected.week,
                region=selected.ara,
                search_keyword=selected.schl_nm,
            )
        ),
        headers={
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    )

    json = response.json()
    return [MealsDetail(**value) for value in json['list']]

def to_dict(detail):
    return {
        value.week_day: value.lunch if value.lunch else '등록된 식단 정보가 없습니다.' for value in detail
    }