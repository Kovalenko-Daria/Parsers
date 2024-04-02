from time import time
import os
import logging
from bs4 import BeautifulSoup
import asyncio
import aiohttp

to_remove = {
    "div": [{"class": "wp-block-lazyblock-link-aside"}, {"class": "accordion"}]
    + [{"class": "wp-block-lazyblock-banner" + str(i)} for i in range(99)]
}


def create_name_file(soup):
    name_file = soup.title.text
    ind = name_file.find(" — Журнал «Код»")
    ind = name_file.find(" — Код") if ind == -1 else ind
    if ind != -1:
        name_file = name_file[:ind]
    name_file = name_file.replace("\xa0", " ")
    for i in '/`~!@#%^&*\\?|"№;:.,][}{()':
        name_file = name_file.replace(i, "")
    return name_file + ".txt"


def clear_code(code, tag, args):
    for c in code.find_all(tag, args):
        c.decompose()


async def add_article(url, el, session):
    async with session.get(url) as response:
        inner_html_code = await response.text()
        soup = BeautifulSoup(inner_html_code, "html.parser")
        name_file = create_name_file(soup)
        with open(rf"статьи\{el}\{name_file}", "w", encoding="utf-8") as file:
            soup = soup.find("div", {"class": "article-content"})
            for key in to_remove:
                for value in to_remove[key]:
                    clear_code(soup, key, value)
            file.write(soup.get_text())
            logging.info(
                f"Article '{name_file}' from {url} has been successfully downloaded"
            )


async def convert_to_articles():
    data_title = ["Ахах", "Не стыдно", "Это баг", "Это как"]
    async with aiohttp.ClientSession() as session:
        page_with_urls = await session.get("https://thecode.media/all")
        soup = BeautifulSoup(await page_with_urls.text(), "html.parser")
        tasks = []
        for dt in data_title:
            os.mkdir(rf"статьи\{dt}")
            logging.info(f"Processing of category '{dt}' has started")
            title_urls = soup.find(attrs={"data-title": dt})
            counter = 0
            for tag in title_urls.select("li:has(a)"):
                task = asyncio.create_task(
                    add_article(tag.find("a")["href"], dt, session)
                )
                tasks.append(task)
                counter += 1
            logging.info(f"{counter} url(s) has(ve) been successfully gathered")

        await asyncio.gather(*tasks)


def main():
    logging.basicConfig(
        level=logging.INFO,
        filename="async_parse_yandex_code_log.log",
        filemode="w",
        encoding="utf-8",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    start = time()
    logging.info("Program has started")
    os.mkdir("статьи")
    asyncio.run(convert_to_articles())

    logging.info(f"Program was completed in {time() - start}s")


if __name__ == "__main__":
    main()
