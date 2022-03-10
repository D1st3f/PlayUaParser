import requests
from bs4 import BeautifulSoup

print()
print('If you want parse news - print "novyny"')
print('If you want parse reviews - print "oglyady"')
print('If you want parse posts - print "statti"')
print('If you want parse videos - print "video"')
print('If you want parse podcasts - print "podcasts"')
print()

type = input("Input type of content: ")


URL = 'https://playua.net/'+type+'/'
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

def main():
    news = parse()
    print_to_file(news)


def print_to_file (news):

    create_line = ""
    for new in news:
        create_line=create_line+new["title"]+"\n"+new["date"]+"\n"+new["text"]+"\n"+new["url"]+"\n"
        create_line = create_line + "\n"+ "\n"
    name = type+".txt"
    file = open(name, "w", encoding="utf-8")
    file.write(create_line)
    file.close()


def get_html(url,params=None):
    r = requests.get(url,headers=HEADERS, params=params)
    return r

def get_pages_count():
    pages = int(input("Enter number of pages: "))
    return pages


def parse ():
    html=get_html(URL)
    if html.status_code== 200:
        news = get_content(html)
        pages = get_pages_count()
        print("Parsing 1 from "+str(pages) )
        for page in range(2, pages + 1):
            print("Parsing "+str(page)+ " from " +str(pages))
            html = get_html(URL,params={"page":page})
            news.extend(get_content(html))

        return (news)

    else:
        print("Error")

def get_content(html):
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all("div", class_="row d-flex align-items-center")
    news = []
    for item in items:
        news.append({
            "title": item.find("h3", class_="short-article__info__title").text.replace("\n",""),
            "date": item.find("time", class_="icon-time short-article__info__other--time").text,
            "text": item.find("div", class_="short-article__description").text.replace("\xa0"," "),
            "url": item.find('a', href=True).get("href").strip(),
        })
    return news

if __name__ == "__main__":
    main()
