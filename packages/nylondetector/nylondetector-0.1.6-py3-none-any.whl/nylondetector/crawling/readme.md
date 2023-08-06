# 개요

기존에 selenium을 이용한 네이버 크롤링 코드를 async 방식으로 개선한 코드이다.

관련된 내용을 정리해 둔다.

# 구조 및 개선점

- 네이버 검색페이지 URL 크롤링
  - 기존
    - process 단위 실행이 무거움
    - 페이지 끝을 sync방식으로 키 입력으로 획득
    - DOM 파싱 비용이 비싼편
  - 개선
    - 코루틴 기반 asyncio, aiohttp 실행
    - 휴리스틱하게 페이지 획득 후 deduplicate
    - 경량인 bs4 파서 사용
    - 1년 단위에서 1달 단위 크롤링 변경 -> 크롤링 문서 증가
- 네이버 블로그 본문 크롤링
  - 기존
    - 블로그 url 접속 -> iframe 이동 -> 2단계 처리
    - selenium 기반 동작 방식
    - blog url을 변수로 받아 바로 처리
  - 개선
    - 블로그 url을 iframe url로 규칙에 맞춰 이동 -> 1단계 처리
    - async 기반 동작 방식
    - csv 산출문서 경로에 접근하여 처리 -> 데이터 작업의 모듈화

# 사용법

아래 3가지 단계로 실행하면 되고 산출물은 `./crawl_data`에 저장된다.

```
$ python3 crawl_url.py
$ python3 deduplicate_url.py
$ python3 crawl_content.py
```
