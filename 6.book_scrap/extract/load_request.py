import requests


def get_next_page_url(url: str, next_url: str):
    if next_url in "":
        return ""
    elif next_url in "begin":
        return requests.get(url).text
    else:
        url = url.replace(url.split("/")[-1], next_url)
        print(url)
        return requests.get(url).text


def get_page_by_url(url: str):
    if url not in "":
        return requests.get(url).text
    else:
        return ""


url = "https://books.toscrape.com/catalogue/category/books_1/page-1.html"
