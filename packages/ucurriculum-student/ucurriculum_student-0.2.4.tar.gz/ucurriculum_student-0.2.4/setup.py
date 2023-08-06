from setuptools import setup

setup(
    name='ucurriculum_student',
    version='0.2.4',
    license='GNU Affero General Public License v3',
    author="Ignacio Palma",
    author_email='ignacio.palma@uc.cl',
    packages=['ucurriculum_student'],
    url='https://github.com/IgnacioPalma/UCurriculum-Student',
    keywords='scraper',
    install_requires=[
        'uc_sso',
        'selenium',
        'bs4',
        'webdriver_manager'
      ],
)