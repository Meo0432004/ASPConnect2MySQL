import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "extract"))
from load_request import url, get_next_page_url, get_page_by_url

from parsel import Selector

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "serializer"))
from serializer import serialize_to_book_scrap

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "load"))
from config import dbContext

import re

if __name__ == "__main__":
    # print(url)
    page = get_next_page_url(url, "begin")
    # print(page)
    all_query = []
    book_scrap = dbContext()
    book_scrap.connect("book_scrap")
    while page not in "":
        selector = Selector(text=page)
        books = selector.xpath("//ol/li").getall()
        for book in books:
            books_selector = Selector(text=book)
            img = books_selector.xpath("//img/@src").get()
            img = img.replace("../../../", "https://books.toscrape.com/")
            # print(img)
            title = books_selector.xpath("//h3/a/@title").get()
            # print(title)
            price = float(
                books_selector.xpath("//p[@class='price_color']/text()").get()[2:]
            )
            # print(price)
            stock = (
                books_selector.xpath("//p[@class='instock availability']/text()")
                .getall()[1]
                .strip()
                or "Out of stock"
            )
            # print(stock)
            book_link = books_selector.xpath("//h3/a/@href").get()
            book_link = book_link.replace(
                "../../", "https://books.toscrape.com/catalogue/"
            )
            # print(book_link)
            book_page = get_page_by_url(book_link)
            book_selector = Selector(text=book_page)
            # print(book_selector)
            book_desciption = book_selector.xpath("//article/p/text()").get()
            # print(book_desciption)
            book_UPC = book_selector.xpath("//tr/td/text()").getall()[0]
            # print(book_UPC)
            book_type = book_selector.xpath("//tr/td/text()").getall()[1]
            # print(book_type)
            availability = book_selector.xpath("//tr/td/text()").getall()[5]
            availability_number = re.search(r"\((\d+)", availability)
            availability_number = int(availability_number.group(1))
            # print(availability_number)

            number_review = book_selector.xpath("//tr/td/text()").getall()[-1]
            # print(number_review)
            model = serialize_to_book_scrap(
                img,
                title,
                price,
                stock,
                book_link,
                book_UPC,
                book_desciption,
                book_type,
                availability_number,
            )
            query = {
                "img": model.img,
                "title": model.title,
                "price": model.price,
                "stock": model.stock,
                "book_link": model.book_link,
                "BookDetails": {
                    "book_UPC": model.BookDetails.book_UPC,
                    "book_description": model.BookDetails.book_description,
                    "book_type": model.BookDetails.book_type,
                    "availability_number": model.BookDetails.availability_number,
                },
            }
            all_query.append(query)
            # print(end="\n\n")

        next_url = selector.xpath("//a[text()='next']/@href").get() or ""
        print(next_url)
        page = get_next_page_url(url=url, next_url=next_url)
        book_scrap.executeNonQuery(query=all_query, operation="insert_many")

        # just scrap 3 first pages in 50 pages
        if next_url in "page-3.html":
            break
