## ServersCenter - Data Analysis Server

__교내 데이터를 수집하고, API를 통해 분석 결과를 제공하는 서버입니다.__

이 저장소는 ServersCenter의 데이터 분석 서버 소스를 관리하기 위한 저장소입니다.

데이터를 수집하고 분석하기 위한 API 서버이며, 회원 관리를 위한 API 등을 포함합니다.

분석 데이터는 HTTP Protocol을 통한 REST API로 제공하며, Web Server와 Android Application에서는 이 API를 가지고 서비스를 제공합니다. 이를 이용한 챗봇 서비스를 통해 사용자는 교내 정보를 쉽게 알 수 있습니다.

## Package

* Flask (Flask/1.0.2) - API Server
* Flask-restful (Flask-RESTful/0.3.6) - API Server
* PyMySQL (PyMySQL/0.9.2)
* SQLAlchemy (SQLAlchemy/1.2.12) - ORM
* numpy (numpy/1.15.2) - Data Analysis
* pandas (pandas/0.23.4) - Data Analysis
* selenium (selenium/3.14.1) - Crawling
* BeautifulSoup (bs4/0.0.1, beautifulsoup4/4.6.3) - Crawling
* lxml (lxml/4.2.5)
* mysqlclient (mysqlclient/1.3.13, mysql 필요)
* sklearn (sklearn/0.0) - Data Analysis
* mecab (python-mecab-ko/1.0.4) - Data Analysis
* request (request/1.0.2)
* xlrd (xlrd/1.1.0)

