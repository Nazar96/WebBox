from webbox.webbox_generator import WebBoxGenerator
from utils.link_generator import generate_sparkinterfax_links
from pathlib import Path
import shutil

companies = [
    'Газпром',
    'Роснефть',
    'Лукойл',
    'Сургутнефтегаз',
    'НОВАТЭК',
    'Сбербанк',
    'Транснефть',
    'Норникель',
    'ВТБ',
    'Татнефть',
    'Россети',
    'НЛМК',
    'Полюс',
    'Северсталь',
    'Интер',
    'АФК',
    'ММК',
    'Магнит',
    'Мосбиржа',
    'Алроса',
    'Аэрофлот',
    'Полиметалл'
]

screen_path = './data/image/'
markup_path = './data/annot/'

shutil.rmtree(screen_path, ignore_errors=True)
shutil.rmtree(markup_path, ignore_errors=True)

Path(screen_path).mkdir(parents=True, exist_ok=True)
Path(markup_path).mkdir(parents=True, exist_ok=True)

links = generate_sparkinterfax_links(companies).values()
links = list(filter(lambda x: x is not None, links))

wbx = WebBoxGenerator(
    screen_path=screen_path,
    markup_path=markup_path,
    sleep_time=0.1
)

wbx.generate(links[:2], 'bbox', max_anchors=5)
