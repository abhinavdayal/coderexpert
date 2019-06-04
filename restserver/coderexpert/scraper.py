# Here all web scraping logic shall be coded
import requests
from lxml import html as HTML
from lxml import etree

def getGeeksForGeeksQuestionDetail(url):
    d = {}
    try:
        html = requests.get(url)
        doc = HTML.fromstring(html.content)
        title_container = doc.xpath('//div[@class="container-fluid"]')[1]
        d['title'] = title_container.xpath('//strong')[0].text_content().strip()
        d['tags'] = [t.text_content().strip() for t in title_container.xpath('.//a[contains(@class, "topicTags")]')]
        anchors = title_container.xpath('.//a')
        sublink = anchors[0].get('href')
        d['pid'] = sublink[sublink.rindex('=')+1:]
        d['level'] = anchors[1].text_content().strip()
        d['accuracy'] = float(title_container.xpath('.//p')[0].text_content().strip()[:-1])
        ps = doc.xpath('.//div[@class="problemQuestion"]')[0]
        d['problemhtml'] = etree.tostring(ps).strip()
    except Exception as e:
        raise RuntimeError('Error scraping the path') from e
    finally:
        return d





