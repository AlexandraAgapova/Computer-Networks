import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class BookParser:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # запуск без графического интерфейса
        options.add_argument(
            "--disable-gpu"
        )  # отключение использования видеокарты в Chrome
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.baseUrl = "http://books.toscrape.com/catalogue/page-{}.html"
        self.results = []
        self.csvFile = "parser.csv"
        self.pageLimit = 3

    def loadPage(self, pageNumber):
        pageUrl = self.baseUrl.format(pageNumber)
        self.driver.get(pageUrl)
        time.sleep(2)  # время на загрузку

    def parsePage(self):
        books = self.driver.find_elements(By.CSS_SELECTOR, "article.product_pod")

        for book in books:
            title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
            price = book.find_element(By.CSS_SELECTOR, "p.price_color").text.strip()
            rating = (
                book.find_element(By.CSS_SELECTOR, "p.star-rating")
                .get_attribute("class")
                .split()[-1]
            )
            url = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")

            self.results.append((title, price, rating, url))

    def saveToCsv(self):
        with open(self.csvFile, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Title", "Price", "Rating", "URL"])
            writer.writerows(self.results)

    def run(self):
        for page in range(1, self.pageLimit + 1):
            self.loadPage(page)
            self.parsePage()

        self.driver.quit()
        self.saveToCsv()


parser = BookParser()
parser.run()
