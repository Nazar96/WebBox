import wikipediaapi
import random
from dask import delayed, compute
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


@delayed
def get_wiki_url(wikipage):
    try:
        url = wikipage.fullurl
        return url
    except KeyError:
        return None


def generate_wiki_links(n=10, start_page='Python', language='ru'):
    wiki = wikipediaapi.Wikipedia(language)

    visited_pages = set()
    new_pages = set()

    start_page = wiki.page(start_page)
    assert start_page.exists(), True

    page = start_page

    while len(new_pages) < n:
        links = set(page.links.values())
        new_pages.update(links)
        page = random.sample(new_pages, 1)[0]

    new_pages = random.sample(new_pages, len(new_pages))

    result = []
    n_trials = len(new_pages) // n
    for i in range(n_trials):
        dask_res = compute(*map(get_wiki_url, new_pages[n * i:n * (i + 1)]))
        dask_res = list(filter(lambda url: url is not None, dask_res))
        result += dask_res
        if len(result) >= n:
            break

    return result[:n]


def get_sparkinterfax_url(name):
    url = 'https://www.spark-interfax.ru/search?Query=' + name
    content = BeautifulSoup(requests.get(url).content)
    try:
        link = content.li.a['href']
        link = urljoin('https://www.spark-interfax.ru/', link)
        return link
    except AttributeError:
        pass


def generate_sparkinterfax_links(companies):
    result = {}
    for company in companies:
        url = get_sparkinterfax_url(company)
        if url is not None:
            result[company] = url
    return result
