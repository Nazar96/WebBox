import wikipediaapi
import random
from dask import delayed, compute

@delayed
def get_url(wikipage):
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
    n_trials = len(new_pages)//n
    for i in range(n_trials):
        dask_res = compute(*map(get_url, new_pages[n*i:n*(i+1)]))
        dask_res = list(filter(lambda url: url is not None, dask_res))
        result += dask_res
        if len(result) >= n:
            break
    
    return result[:n]
