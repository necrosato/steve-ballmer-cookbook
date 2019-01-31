import wikipedia
import re
from bs4 import BeautifulSoup as bs

def main():
    list_of_cocktails = wikipedia.page("List of cocktails")
    i = 0
    for link in list_of_cocktails.links:
        page = wikipedia.page(link)
        print(page.title)
        soup = bs(page.html(), 'html.parser')
        print(soup.find_all("table", "infobox"))
        i+=1
        if i > 1:
            break


if __name__ == "__main__":
    main()
