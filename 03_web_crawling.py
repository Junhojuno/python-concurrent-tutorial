"""yes24에서 파이썬 관련 전체 출간도서(신상품 순서) 정보 가져오기"""
from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def fetcher(session, url):
    """페이지 번호별 정보 가져오는 기능"""
    async with session.get(url) as response:
        html = await response.text()
        await html_parser(html)


async def html_parser(html):
    """페이지 내 도서명 추출"""
    soup = BeautifulSoup(html, 'html.parser')
    content_area = soup.find('div', 'cCont_listArea').find('ul', 'clearfix')
    content_ls = content_area.find_all('div', 'cCont_goodsSet')
    for content in content_ls:
        goods_name = content.find('div', 'goods_name').find('a').text
        if goods_name is not None:
            print(goods_name)


async def main(base_url, n_page=10):
    urls = [f'{base_url}&PageNumber={page_number}' for page_number in range(1, n_page + 1)]
    async with aiohttp.ClientSession() as sess:
        results = await asyncio.gather(
            *[fetcher(sess, url) for url in urls]
        )


if __name__ == '__main__':
    asyncio.run(
        main('http://www.yes24.com/24/Category/Display/001001003022004?ParamSortTp=04', 10)
    )
