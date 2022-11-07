from loguru import logger
from bs4 import BeautifulSoup
import re, json

@logger.catch
def prettify():
    with open("./高レベル非公式難易度（FC基準） - Deemo Wiki .html") as fp:
        soup = BeautifulSoup(fp)

    with open("./prettified.html", "w") as wfp:
        wfp.write(soup.prettify())

@logger.catch
def getDict(soup):
    Divlist = soup.find_all("div", "h-scrollable")
    Dict = {}
    for i in Divlist:
        titlesoup = i.find_previous("h4")
        level = titlesoup.get_text().split("v")[1].split("(")[0]
        ptrsoup = i.table.tbody.tr.next_sibling.next_sibling
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

        Dict[level] = ResList
    return Dict

#prettify()

with open("./prettified.html") as fp:
    soup = BeautifulSoup(fp)

with open("./RawDict.json", "w") as fp:
    json.dump(getDict(soup), fp, ensure_ascii=False, indent=4)
