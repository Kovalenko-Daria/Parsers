from time import time
import os
import logging
import requests
from bs4 import BeautifulSoup

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


def add_article(url, el):
    inner_html_code = requests.get(url)
    soup = BeautifulSoup(inner_html_code.text, "html.parser")
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


def get_all_urls_with_title(data_title):
    page_with_urls = requests.get("https://thecode.media/all")
    soup = BeautifulSoup(page_with_urls.text, "html.parser")
    title_urls = soup.find(attrs={"data-title": data_title})
    urls = []
    counter = 0
    for tag in title_urls.select("li:has(a)"):
        urls.append(tag.find("a")["href"])
        counter += 1
    logging.info(f"{counter} url(s) has(ve) been successfully gathered")
    return urls


def convert_to_articles():
    division = ["Ахах", "Не стыдно", "Это баг", "Это как"]
    for el in division:
        logging.info(f"Processing of category '{el}' has started")
        urls = get_all_urls_with_title(el)
        os.mkdir(rf"статьи\{el}")
        for url in urls:
            add_article(url, el)


def main():
    logging.basicConfig(
        level=logging.INFO,
        filename="sync_parse_yandex_code_log.log",
        filemode="w",
        encoding="utf-8",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    start = time()
    logging.info("Program has started")
    os.mkdir("статьи")
    convert_to_articles()

    logging.info(f"Program was completed in {time() - start}s")


if __name__ == "__main__":
    main()
