import asyncio
import json
from pathlib import Path
from typing import TypedDict, List

from playwright.async_api import async_playwright
from tqdm import tqdm

HEADLESS = True  # False: 打开浏览器（调试时建议使用） / True: 浏览器在后台运行
POSITION_LIST_URL = "https://www.evtol.news/aircraft"

# 用于获取evtol二级链接的js脚本，返回一个evtol链接列表: List[str]
spider_js = Path("./spider.js").read_text(encoding="utf-8")

# 在evtol详情页，解析evtol信息的js脚本，返回一个字典: Dict[str, str]
parse_js = Path("./parse.js").read_text(encoding="utf-8")

# 输出目录
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class Info(TypedDict):
    title: str
    url: str
    Specifications: List[str]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS, slow_mo=200, timeout=0)

        page = await browser.new_page()

        await page.goto(POSITION_LIST_URL)
        evtol_urls = await page.evaluate(spider_js)

        print("获取到的evtol链接数量为：", len(evtol_urls))

        info_lst = []
        url_iterator = tqdm(evtol_urls)
        for evtol_url in url_iterator:
            try:
                url_iterator.set_description(f"正在爬取的网址：{evtol_url}")
                await page.goto(evtol_url)
                info = Info(**(await page.evaluate(parse_js)))
                info_lst.append(info)

                postfix = f"{info['title']}获取到{len(info['Specifications'])}条信息"
                url_iterator.set_postfix_str(postfix)

            except Exception as e:
                print(f"获取 {evtol_url} 信息失败：", e)

        with open(OUTPUT_DIR / 'output.json', 'w') as file:
            json.dump(info_lst, file, indent=4)


if __name__ == '__main__':
    asyncio.run(main())
