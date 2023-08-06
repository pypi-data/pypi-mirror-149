from setuptools import setup

setup(
    name='foodsafetykorea',
    version='1.0.0',
    description='평범한 중학생이 만든 비공식 foodsafetykorea를 이용한 학교 급식을 알려주는 패키지입니다.',
    long_description='# Usage\n```shell\npython -m foodsafetykorea.command --region 인천광역시 우리학교\n```\n## 정보\n문제될 시 삭제합니다.',
    long_description_content_type='text/markdown',
    author='LUA9',
    maintainer='LUA9',
    packages=['foodsafetykorea']
)