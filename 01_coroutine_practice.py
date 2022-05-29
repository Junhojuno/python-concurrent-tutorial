"""web data 크롤링 예제"""
import asyncio
import aiohttp
import time
import requests


def fetcher(session, url):
    """session 결과 반환"""
    with session.get(url) as response:
        return response.text


async def fetcher_async(session, url):
    async with session.get(url) as response:
        return await response.text() # awaitable object


def main():
    """session을 사용하여 네이버의 html정보를 가져오고, 그 상태를 유지한다"""
    urls = ['https://www.naver.com', 'https://www.google.co.kr', 'https://www.tiktok.com'] * 10
    
    with requests.Session() as sess:
        results = [fetcher(sess, url) for url in urls]


async def main_async():
    urls = ['https://www.naver.com', 'https://www.google.co.kr', 'https://www.tiktok.com'] * 10
    
    async with aiohttp.ClientSession() as sess:
        # results = [await fetcher_async(sess, url) for url in urls] # 이건 시간 단축이 안 됨!
        results = await asyncio.gather(
            *[fetcher_async(sess, url) for url in urls]
        )        


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('request time without async: ', end - start)

    # coroutine
    start = time.time()
    asyncio.run(main_async())
    end = time.time()
    print('request time with async: ', end - start)
