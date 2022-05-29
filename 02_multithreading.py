"""
multi-threading with concurrency
    - python에서는 병렬로 multi-threading하는 것이 불가능하다 -> GIL
"""
import time
import requests
import os
import threading
from concurrent.futures import ThreadPoolExecutor


def fetcher(session, url):
    """session 결과 반환
    
    어떤 process, 어떤 thread에서 사용되는지 확인
    """
    print(
        f'{os.getpid()} process | {threading.get_ident()} url: {url}'
    )
    with session.get(url) as response:
        return response.text


def main():
    """session을 사용하여 네이버의 html정보를 가져오고, 그 상태를 유지한다"""
    urls = ['https://www.naver.com', 'https://www.google.co.kr', 'https://www.tiktok.com'] * 10
    
    with requests.Session() as sess:
        results = [fetcher(sess, url) for url in urls]

# ---- multi threading
def fetcher_multithreading(params):
    """session 결과 반환
    
    어떤 process, 어떤 thread에서 사용되는지 확인
    """
    session, url = params
    print(
        f'{os.getpid()} process | {threading.get_ident()} url: {url}'
    )
    with session.get(url) as response:
        return response.text


def main_multithreading():
    urls = ['https://www.naver.com', 'https://www.google.co.kr', 'https://www.tiktok.com'] * 10
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        with requests.Session() as sess:
            params = [(sess, url) for url in urls]
            executor.map(fetcher_multithreading, params)



if __name__ == '__main__':
    # start = time.time()
    # main()
    # end = time.time()
    # print('request time without async: ', end - start)
    
    start = time.time()
    main_multithreading()
    end = time.time()
    print('request time with multi-threading: ', end - start)
