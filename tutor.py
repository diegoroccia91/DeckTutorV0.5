import requests
import os
import shutil
from bs4 import BeautifulSoup


# Busca el meta de un formato
# Devuelve lista de tuplas --> (deck_url, deck_name)
def getMeta(URL_BASE, wntdFormat):
    res = []
    URL = URL_BASE + f"/metagame/{wntdFormat}#paper"
    page = requests.get(URL).text
    soup = BeautifulSoup(page, "lxml")
    linkData = soup.find(
        id="metagame-decks-container").find_all(class_="deck-price-paper")
    for elem in linkData:
        data = elem.find("a")
        if str(data) != "None":
            res.append((data.get("href"), data.get_text()))
    return res


# Scrap deck
# devuelve una lista de listas de tuplas, lista[0]mainDeck | lista[1]SideBoard
def getDeck(URL_BASE, deck):
    res = [[], []]
    flagDeck = 0
    URL = URL_BASE + deck
    page = requests.get(URL).text
    soup = BeautifulSoup(page, "lxml")
    link_info = soup.find(class_="deck-view-deck-table").find_all("tr")
    for elem in link_info:
        # buscando el inicio del side
        if elem.has_attr("class"):
            if elem.get_text().split()[0] == "Sideboard":
                flagDeck = 1  # marcar el inicio del sideboard
        else:
            data = elem.find(class_="text-right").get_text().strip()
            cardName = elem.find("a").get_text().strip()
            res[flagDeck].append((data, cardName))
    return res


def removeDuplicate(deckLink):
    visited = []
    pointerList = []
    pointer = -1
    for _, name in deckLink:
        pointer += 1
        if name in visited:
            pointerList.append(pointer)
        else:
            visited.append(name)
    pointer = 0  # re use as offset
    for x in pointerList:
        del deckLink[x - pointer]
        pointer += 1


def deckCreator(path, name, deck):
    filePath = os.path.join(path, f"{name}.cod")
    f = open(filePath, "w+")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<cockatrice_deck version=\"1\">\n")
    f.write(f"\t<deckname>{name}</deckname>\n")
    f.write("\t<comments></comments>\n")
    f.write("\t<zone name=\"main\">\n")
    for x in deck[0]:
        f.write(f"\t\t<card number=\"{x[0]}\" name=\"{x[1]}\"/>\n")
    f.write("\t</zone>\n")
    f.write("\t<zone name=\"side\">\n")
    for x in deck[1]:
        f.write(f"\t\t<card number=\"{x[0]}\" name=\"{x[1]}\"/>\n")
    f.write("\t</zone>\n")
    f.write("</cockatrice_deck>\n")
    f.close()


def createFormat(BASE_PATH, wntdFormat, component):
    URL_BASE = "https://www.mtggoldfish.com/"
    path = os.path.join(BASE_PATH, wntdFormat)
    component.addText(f"Downloading {wntdFormat.capitalize()} decks")
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
    metaList = getMeta(URL_BASE, wntdFormat)
    removeDuplicate(metaList)
    for index, entry in enumerate(metaList):
        component.addText(f"Deck {index+1}/" + str(len(metaList)))
        deck = getDeck(URL_BASE, entry[0])
        deckCreator(path, entry[1], deck)
    component.addText("")


def deckTutor(path_download, wanted_formats, component):
    FORMATS = ["standard", "modern", "pioneer", "pauper", "legacy", "vintage"]
    to_create = []
    if not os.path.exists(path_download):
        os.makedirs(path_download)

    for x in range(len(wanted_formats)):
        if wanted_formats[x].get() == 1:
            to_create.append(FORMATS[x])
    for wntdFormat in to_create:
        try:
            createFormat(path_download, wntdFormat, component)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except Exception as e:
            raise SystemExit(e)
    component.addText("Finish")


def getPath():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "decks")
