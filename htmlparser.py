from loguru import logger
from bs4 import BeautifulSoup
import re

@logger.catch
def prettify():
    with open("./高レベル非公式難易度（FC基準） - Deemo Wiki .html") as fp:
        soup = BeautifulSoup(fp)

    with open("./prettified.html", "w") as wfp:
        wfp.write(soup.prettify())

#@logger.catch
def getList(soup):
    """
    Argument soup is the h4 soup containing title.
    e.g. <h4 class=...> Lv7.2 ... </h4>.
    Return: [["曲名", "Diff", ..., "Version", "Comment"], ...]
    """
    try:
        titlesoup = soup.table.tbody.tr # Normal
    except:
        retry = 40
        titlesoup = soup
        while(titlesoup.name != "div" and retry > 0):
            retry = retry - 1
            titlesoup = titlesoup.next_sibling
            logger.warning(titlesoup)
            try:
                if titlesoup["class"] != "h-scrollable":
                    continue
                titlesoup = titlesoup.table.tbody.tr
                break
            except:
                continue
    ptrsoup = titlesoup.next_sibling.next_sibling
    TempList = []
    ResList = []
    while(1):
        try:
            if ptrsoup.name != "tr":
                break
        except:
            break
        oneList = []
        for i in ptrsoup.contents:
            try:
                text = i.get_text().strip().replace("\n            ", "")
                oneList.append(text)
            except:
                pass
        TempList.append(oneList)
        ptrsoup = ptrsoup.next_sibling.next_sibling

    for i in range(len(TempList)):
        if i % 2:
            ResList[-1].append(TempList[i][0])
        else:
            ResList.append(TempList[i])
    #print(ResList)
    return ResList


#prettify()
with open("./prettified.html") as fp:
    soup = BeautifulSoup(fp)
Dict = {}
#titlesoup = soup.h4
titleList = soup.find_all("h4")
for titlesoup in titleList:
    level = titlesoup.get_text().split("v")[1].split("(")[0]
    #try:
    #    Dict[level] = getList(titlesoup.next_sibling.next_sibling)
    #except AttributeError:
        #Dict[level] = getList(titlesoup.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling)
        #pass
    Dict[level] = getList(titlesoup.next_sibling.next_sibling)
print(Dict)
