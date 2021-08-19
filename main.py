from urllib.request import Request as rq
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from bs4.element import Tag

""" this short program serves as a future reference for building webscrappers.
    it:
        1. retrieves the request from a given address, converts it to raw html(?) and soupifies it
        2. separates the wiki's 'contents' tab to work on it
        3. from that 'contents' tab it then finds all chapters and subchapters tags and puts them in a nice list"""

def wrap_nicely(link: str, heading: str, first_par: str, contents: Tag) -> None:
    print(f'Summary of {link} :\n')

    #using ANSI escape sequences
    print(f'\033[4m{heading}\033[0m \n')

    print(f'{first_par} \n')

    for chptr in contents:
        indent = "  " * chptr[0].count('.')
        print(f'{indent}{chptr[0]} {chptr[1]}')

def get_text_no_subscribts(tag: Tag) -> str:
    subscripts = tag.find_all('sup')

    for subcr in subscripts:
        subcr.decompose()
    
    return tag.get_text()

def main():

    uerel = 'https://en.wikipedia.org/wiki/Special:Random'

    """ an important note: you can theoretically omit the 'req' variable and just pass the URL into urlopen().
        However, not requesting the page via the Requests lib won't authenticate(?) your request, so 403 error may occur."""

    req = rq(uerel, headers={'User-Agent': 'Mozilla/5.0'}) #fetch request with authentication (see above)
    raw = urlopen(req).read() #convert to raw (byte literal) html
    soup = bs(raw, 'lxml') #make a soup

    """getting the url, heading, summary and contents tab"""
    #to get the URL adress of a random wiki page, get a <link> tag with rel="canonical" and retrieve its href text
    url = soup.find('link', rel="canonical").attrs['href']

    heading = soup.find('h1', id="firstHeading").text

    summary = get_text_no_subscribts(soup.find('div', class_="mw-parser-output").p)

    contents = soup.find('div', class_="toc", role='navigation') #gets the contnents tab

    try:
        chapter_text_list = [tx.text for tx in contents.find_all('span', class_='toctext')]
        chapter_number_list = [nu.text for nu in contents.find_all('span', class_='tocnumber')]
        
    except AttributeError:
        print(f"{url} has no 'Contents' tab.")
        return 0
    else:
        chapters = list(zip(chapter_number_list, chapter_text_list))
        
    wrap_nicely(url, heading, summary, chapters)
    
    return 1


if __name__ == "__main__":
    main()