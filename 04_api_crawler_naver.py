"""네이버 API를 활용하여 이미지 정보 가져오기"""
import asyncio
import aiohttp
from pprint import pprint
from load_config import get_secret


async def fetcher(session, url):
    """json형태의 정보에서 이미지 파일 정보 추출"""
    headers = {
        'X-Naver-Client-Id': get_secret('NAVER_API_ID'),
        'X-Naver-Client-Secret': get_secret('NAVER_API_KEY')
    }
    
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result['items'] # list type
        images = [item['link'] for item in items] # image links
        pprint(images)
        

async def main(base_url, keyword, n_displays=1, n_pages=1):
    urls = [f'{base_url}?query={keyword}&display={n_displays}&start={i * 20 + 1}' for i in range(n_pages + 1)]
    async with aiohttp.ClientSession() as sess:
        await asyncio.gather(
            *[fetcher(sess, url) for url in urls]
        )


if __name__ == '__main__':
    asyncio.run(
        main(
            base_url='https://openapi.naver.com/v1/search/image',
            keyword='dog',
            n_displays=10,
            n_pages=1
        )
    )
