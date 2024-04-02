# Parsers

## About
A set of parsers for solving personal practical problems
***

## Parsers

* _Article parser async_ and _Article parser async_<br>

Both parsers are implemented to download articles from the Yandex Journal "Code", but they are implemented using different approaches.

_Article parser async_ does everything asynchronously. For each of the required pages are created tasks, which are saved in the event loop that is being launched 
Libraries used: asyncio, aiohttp, bs4 (BeautifulSoup), time, os, logging

_Article parser sync_ does everything synchronously. For each required page, data is sequentially requested, which is then written to files.
Libraries used: requests, bs4 (BeautifulSoup), time, os, logging