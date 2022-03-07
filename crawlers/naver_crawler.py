import aiohttp
import asyncio
import aiofiles
import os
import urllib.request
import re
import time
from config import get_secret


async def img_downloader(session, img):
    img_name = re.sub('[\/:*?"<>|]', "", (img.split("/")[-1]))
    try:
        os.mkdir(f"./images_{input_keyword}")
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(
                f"./images_{input_keyword}/{img_name}", mode="wb"
            ) as file:
                img_data = await response.read()
                await file.write(img_data)


async def fetch(session, url, i):
    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET")
    }
    try:
        async with session.get(url, headers=headers) as response:
            result = await response.json()
            items = result["items"]
            images = [item["link"] for item in items]
            print(i + 1)
            await asyncio.gather(*[img_downloader(session, img) for img in images])
    except Exception as ex:
        print(ex)
        pass


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    urls = [
        f"{BASE_URL}?query={keyword}&display=50&start={1 + i*50}" for i in range(1, 11)
    ]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":
    input_keyword = input("얻고자 하는 이미지 키워드 : ")
    start = time.time()
    keyword = urllib.parse.quote(input_keyword)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end = time.time()
    print("걸린 시간 : ", end - start)