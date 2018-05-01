import urllib.request
from bs4 import BeautifulSoup
import sys
import io
import pathlib


def getHtmlObject(URL):

    request         = urllib.request.Request(URL)
    request.add_header('User-Agent', 'Mozilla/5.0')
    response        = urllib.request.urlopen(request)

    return response


def getBs4Object(htmlObject):

    bs4Object       = BeautifulSoup(htmlObject, "html.parser")

    return bs4Object


def getAllEpisodeURL():

#    URL             = 'http://www.manhuadb.com/manhua/476/484_5149.html'
    URL             = 'http://www.manhuadb.com/manhua/488/497_5414.html'

    htmlObject      = getHtmlObject(URL)
    bs4Object       = getBs4Object(htmlObject)

    episodeButtons  = bs4Object.findAll("a", {"class": "px-1"})


    episodeURL    = []

    for each_button in episodeButtons:

        button_url  = domain + each_button['href']

        episodeURL.append(button_url)

    return episodeURL


def getAllEpisodeNumber():

    allEpisodeNumber      = len(getAllEpisodeURL())

    return allEpisodeNumber


def getEpisodePageNumber(URL):

    htmlObject          = getHtmlObject(URL)
    bs4Object           = getBs4Object(htmlObject)

    nextPageResource    = bs4Object.findAll(attrs={"id": "page-selector"}, limit=1)

    episodePageNumber = 0

    for element in nextPageResource[0]:

        if element != '\n':
            episodePageNumber = episodePageNumber + 1
    # start from 1 but not 0
    return episodePageNumber


def getNextPageURL(URL):

    htmlObject          = getHtmlObject(URL)
    bs4Object           = getBs4Object(htmlObject)

    nextPageDom         = bs4Object.findAll("a", {"class": "pnext"})
    nextPageURL         = domain + nextPageDom[0]['href']

    return nextPageURL


def getPageImage(URL):

    request = urllib.request.Request(URL)
    response = urllib.request.urlopen(request)

    bs_object = BeautifulSoup(response, "html.parser")

    img_resource = bs_object.findAll("img", {"class": "img-fluid"})
    img_url = domain + img_resource[0]['src']

    return img_url


def downloadImage(URL, filename):

    urllib.request.urlretrieve(URL, filename)


def promptUX():

    rangeOrNot = input("Select episode range or not? (y/n) ")

    while(True):

        if rangeOrNot != 'y' and rangeOrNot != 'n':
            rangeOrNot = input("Select episode range or not? (y/n) ")
        else:
            break

    episodeRangeTop     = 0

    if rangeOrNot == 'y':

        while(True):

            print ("(Episode 1 to " + str(allEpisodeNumber) + " )")
            tempTop = input("Range from: ")
            tempBottom = input("Range to: ")

            if tempTop.isnumeric() and tempBottom.isnumeric():
                if int(tempTop) < allEpisodeNumber and int(tempBottom) < allEpisodeNumber:
                    if int(tempTop) > 0 and int(tempBottom) > 0:
                        if int(tempTop) < int(tempBottom):
                            episodeRangeTop = tempTop
                            episodeRangeBottom = tempBottom
                            break
            print ("Ilegal Input \n")



    else:
        episodeRangeTop         = 0
        episodeRangeBottom      = allEpisodeNumber

    dataList                    = []
    dataList.append(episodeRangeTop)
    dataList.append(episodeRangeBottom)

    return dataList


sys.stdout          = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
domain              = 'http://www.manhuadb.com'

allEpisodeURL       = getAllEpisodeURL()
allEpisodeNumber    = getAllEpisodeNumber()

def main():

    comicName               = "island_47"

    dataList                = promptUX()
    episodeRangeTop         = dataList[0]
    episodeRangeBottom      = dataList[1]

    for episodeNumber in range(int(episodeRangeTop), int(episodeRangeBottom)):

        eachEpisodeURL      = allEpisodeURL[episodeNumber]
        episodePageNumber   = getEpisodePageNumber(eachEpisodeURL)


        savedPathName       = pathlib.Path(comicName + "/episode_" + str(episodeNumber + 1) + '/')

        if savedPathName.exists() == False:

            savedPathName.mkdir(parents=True, exist_ok=True)

        print ("Episode " + str(episodeNumber + 1) + " is downloading......")

        tempPageURL         = eachEpisodeURL

        for pageNumber in range(1, episodePageNumber + 1):

            if pageNumber < 10:

                pageNumber  = '0' + str(pageNumber)

            imageURL        = getPageImage(tempPageURL)

            imageName       = str(pageNumber) + ".png"
            tempPageURL     = getNextPageURL(tempPageURL)

            downloadImage(imageURL, str(savedPathName / imageName))


if __name__ == '__main__':

    main()


