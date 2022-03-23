

# Django Ubuntu setting



> AWS 가상머신에서 django app을 이용한 웹사이트 배포



과정 

1. **django <> mysql db연동**

   - 커넥터 설치 

     ```
     pip install mysqlclient
     ```

   - settings.py 설정 변경

     ```
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'test', # 연동할 MySQL의 데이터베이스 이름
             'USER': 'root', # DB 접속 계정명
             'PASSWORD': '1234', # 해당 DB 접속 계정 비밀번호
             'HOST': 'localhost', # 실제 DB 주소
             'PORT': '3306', # 포트번호
         }
     }
     ```

   - 연동된 db table 자동 생성

     ```
     python manage.py inspectdb
     ```

     - 터미널에 연동된 데이터 테이블이 클래스로 나옴
     - 복사해서 models.py 에 붙여넣기

   - views.py 에서 from .models import <class 이름>, <class이름> ... 으로 불러와서 데이터셋 사용하기 (많으면 *로)

   - 다만들고 장고프로젝트에 어떤 패키지들이 깔려있는지 확인하기 (AWS 환경에서 빠르게 구축가능) 

     ```
     Housing/django/housing > pip freeze
     ```

     나오는 내용 복사해서 requirements.txt 로 생성하기 코드

     ```
     pip freeze > requirments.txt
     
     ls 로 생성 확인
     cat 으로 내용 확인
     ```

   - **git push**



​		**ubuntu git 안될때......**

```
pip3 install django

mkdir djangoTest
cd djangoTest

django-admin startproject testsite
cd testsite

python3 manage.py runserver

```



2. **github 이용해 AWS ubuntu에서 django 실행 하기**

   > AWS 들어가서 home/ubuntu $ 까지 잡고 나서 환경 설정인데 학원에서 준 피시는 대부분 깔려있을듯 생략 가능

 - ```
   sudo apt-get update
   sudo apt-get install build-essential
   sudo apt-get install python3
   python3 --version
   sudo apt-get install python3-pip
   sudo pip3 install --upgrade pip
   
   ssh-keygen -t rsa 		#배포할때 쓸 퍼블릭 키 생성 , 비밀번호 생성 'housing4'
   cat /home/ubuntu/.ssh/id_rsa.pub			#생성한 키 확인 복사 깃헙 세팅 deploy keys에 키 추가 올리기 깃헙 다른 사용자들이 이 키로 풀받을수 있음
   ```



- git clone 으로 작업 복사

```
# git clone <ssh 주소>
git clone git@github.com:JungMJ322/Housing.git 
# 비밀번호 'housing4'
```

- 작업 폴더에 가상환경 잡아주기 (받은 가상머신에 콘다 깔려있으므로 콘다 사용)

  ```
  # 가상환경 이름 : venv
  conda create -n venv python=3.7 django
  conda activate venv
  ```

  

- django/housing (장고디렉터리 가서 장고에서 사용한 필요 패키지 설치해주기 해당 위치에 *requirements.txt 로 저장했었음)

  ```
  pip install -r requirements.txt
  ```

- web app(django)와 web server 연결 하거나 / 계속 터미널 돌게 하거나 둘중하나 하는거

  강사님 파일보고 따라하기