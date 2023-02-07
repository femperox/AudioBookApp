from bs4 import BeautifulSoup
import requests
import csv
import os

booksInfo = []
csvFile = 'audioBooks.csv'
if not os.path.exists(csvFile):
    booksInfo.append(['img', 'title', 'author', 'genre', 'desc', 'readers', 'read-time'])

for pg in range(1, 4073): 
        print(f"now: {pg}")
        curl = f'https://knigavuhe.org/new/?page={pg}'

        page = requests.get(curl)
        soup = BeautifulSoup(page.text, "html.parser")

        allBooks = soup.findAll('div', class_='bookkitem')
        
        bookInfo = {}
        
        for book in allBooks:
            if book.find('span', class_='bookkitem_author') and book.find('span', class_='bookkitem_meta_time'):
                bookInfo["img"]= book.find('img', class_='bookkitem_cover_img')['src']
                bookInfo["title"]= book.find('a', class_='bookkitem_name').text[1:]
                bookInfo["author"]= book.find('span', class_='bookkitem_author').text.split('\n')[2].replace('  ', '')[:-1]
                bookInfo["genre"]= book.find('div', class_='bookkitem_genre').text.replace('\n', '').lower()
                bookInfo["desc"]= book.find('div', class_='bookkitem_about').text
                bookInfo["readers"]= book.find('div', class_='bookkitem_meta_block').text.replace('\n', '').replace('Читает', '').replace('Читают', '').replace('  ', '')[:-1]
                bookInfo["read-time"]= book.find('span', class_='bookkitem_meta_time').text 

                booksInfo.append(list(bookInfo.values()))
    
file = open(csvFile, 'a', encoding="utf-8")
writer = csv.writer(file, delimiter =';')
writer.writerows(booksInfo)
file.close()

print(f"Written {len(booksInfo)} lines")
