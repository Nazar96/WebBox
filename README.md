# WebBox
Create text detection data from web pages

## Installation

```bash
pip install .
```

## Usage:
```python

from webbox.webbox_generator import WebBoxGenerator

screen_path = '...'
markup_path = '...'

wbg = WebBoxGenerator(
            screen_path=screen_path,
            markup_path=markup_path,
            sleep_time=0.1,
        )
 links = ['https://ru.wikipedia.org/wiki/']
 
 # Generate bounding boxes
 wbg.generate(links, 'bbox')
 
 # Generate heatmaps
 wbg.generate(links, 'heatmap')
 ```
