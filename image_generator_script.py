from webbox.webbox_generator import WebBoxGenerator
from utils.link_generator import generate_wiki_links
from pathlib import Path
import shutil

N_LINKS = 500
screen_path = './data/image/'
markup_path = './data/annot/'

shutil.rmtree(screen_path, ignore_errors=True)
shutil.rmtree(markup_path, ignore_errors=True)

Path(screen_path).mkdir(parents=True, exist_ok=True)
Path(markup_path).mkdir(parents=True, exist_ok=True)

links = generate_wiki_links(N_LINKS)

wbx = WebBoxGenerator(
    screen_path=screen_path,
    markup_path=markup_path,
    sleep_time=0.1
)

wbx.generate(links, 'bbox', max_anchors=5)
