from aiohttp import ClientSession
from pyquery import PyQuery
from sys import argv
from downloader import main
from time import sleep
from asyncio import get_event_loop

web = ClientSession()

def ruc(coro):
    return get_event_loop().run_until_complete(coro)

def id_from_link(link):
    return link.split("/")[2]

def get_episodes(aid):
    page = 1
    ids = []
    while True:
        res = ruc(web.get("https://www.antenna.gr/templates/data/morevideos", params={"aid":aid, "p":page}))
        if res.status == 200:
            root = PyQuery(ruc(res.text()))
            l= []
            for el in root.find("article"):
                el = el.find("a")
                link = el.attrib["href"]
                l.append(id_from_link(link))
            ids.extend(l)
            if not l:
                break
        page+=1
    return ids
        

if __name__ == '__main__':
    ids = get_episodes(argv[1])
    for i in ids:
        main(i)