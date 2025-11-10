import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://openlibrary.org/search?q=subject_key%3A%22thrillers%22"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

titles = soup.find_all("a", class_="results", itemprop="url")
authors = soup.find_all("span", class_="bookauthor")
publish_info = soup.find_all("span", string=lambda text: text and "First published" in text)
editions = soup.find_all("a", href=lambda x: x and "#editions-list" in x)
ratings = soup.find_all("span", itemprop="ratingValue")


data = {
    'Title': [],
    'Author': [],
    'Publish Year': [],
    'Editions': [],
    'Rating': []
}

for i in range(len(titles)):
    title = titles[i].text.strip() if i < len(titles) else "N/A"

    author = "N/A"
    if i < len(authors):
        author_tag = authors[i].find("a")
        author = author_tag.text.strip() if author_tag else "N/A"

    year = "N/A"
    if i < len(publish_info):
        year = publish_info[i].text.strip().replace("First published in", "").strip()

    edition = "N/A"
    if i < len(editions):
        edition = editions[i].text.strip()

    rating = "N/A"
    if i < len(ratings):
        rating = ratings[i].text.strip()

    data['Title'].append(title)
    data['Author'].append(author)
    data['Publish Year'].append(year)
    data['Editions'].append(edition)
    data['Rating'].append(rating)

df = pd.DataFrame(data)

df.to_csv("Thriller_books_detailed.csv", index=False, encoding="utf-8")

