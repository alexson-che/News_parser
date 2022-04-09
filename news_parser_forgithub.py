mtsLink = 'https://www.mts.by/news/'
a1Link = 'https://www.a1.by/ru/company/c/news'
minby = 'https://mpt.gov.by/ru/news'
beltel = 'https://beltelecom.by/news'
becloud = 'https://becloud.by/media-center/news/'
mts_arm = 'https://www.mts.am/ru/Individual-customers/news'
beeline_am = 'https://www.beeline.am/hy/news'
ucom = 'https://www.ucom.am/ru/news'
psrc = 'https://psrc.am/static/news'

print('Введите начальную дату в формате (YYYYMMDD)')
beginfrom = str(input())

import datetime, locale  # для обработки строки с датой новости
import requests
import re  # библиотеке регулярок для очистки текста
import subprocess  # для прохода прокси
import smtplib, time, mimetypes

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))  # для обработки строки с датой новости
time = str(time.strftime("%Y-%m-%d; %H:%M;", time.localtime()))
print(time)

from bs4 import BeautifulSoup


CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  # функция чистит html


def cleanhtml(raw_html):  # функция чистит html
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


import pandas as pd

# ___________________________________________________
try:

    session = requests.Session()
    response = session.get(mtsLink, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)
    soup = BeautifulSoup(response.content, 'html.parser')

    # result = requests.get(mtsLink, verify=True)
    # soup = BeautifulSoup(result.content, 'html.parser')

    links = []
    data = []

    for elem in soup.select('.page-news__title a'):
        links.append('https://www.mts.by/' + elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'BY'
        card['provider'] = 'MTS'
        card['title'] = soup.select('.row.page-aside-wrap h1')[0].text.strip()
        date_clean = datetime.datetime.strptime(soup.select('.page-article__date')[0].text.strip(),
                                                '%d.%m.%Y')  # обрабатываем строку для получения даты
        card['date'] = date_clean
        textrow = soup.select('p')
        raw_html = "".join([str(n) for n in textrow])
        card['news_text'] = cleanhtml(raw_html)
        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))

    df_MTS = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные

    df_MTS.head(30)
    df_MTS = df_MTS[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_MTS

except:
    print(mtsLink, 'link is missed')

# ___________________________________________________
try:
    session = requests.Session()
    response = session.get(a1Link, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    data = []

    for elem in soup.select('.article-listing-item a'):
        links.append('https://www.a1.by' + elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'BY'
        card['provider'] = 'A1'
        card['title'] = soup.select('.col-sm-12 h1')[0].text.strip()
        date_clean = datetime.datetime.strptime(soup.select('.news-item-date')[0].text.strip(),
                                                '%d.%m.%Y')  # обрабатываем строку для получения даты
        card['date'] = date_clean
        textrow = soup.select('p')  # удалить "наши консультанты" из результата
        raw_html = "".join([str(n) for n in textrow])
        card['news_text'] = cleanhtml(raw_html)
        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))

    df_A1 = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_A1.head(30)
    df_A1 = df_A1[['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_MTS.append(df_A1, ignore_index=True)

    del df_A1
except:
    print(a1Link, 'link is missed')
# ___________________________________________________
try:
    session = requests.Session()
    response = session.get(minby, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    data = []

    for elem in soup.select('.news-item-title a'):
        links.append('https://mpt.gov.by' + elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'BY'
        card['provider'] = 'Minsvyazi-BY'
        card['title'] = soup.select('.title')[0].text.strip()
        date_clean = datetime.datetime.strptime(soup.select('.field-item.even')[0].text.strip(),
                                                '%d.%m.%Y')  # обрабатываем строку для получения даты
        card['date'] = date_clean
        textrow = soup.select('p')
        raw_html = "".join([str(n) for n in textrow])
        card['news_text'] = cleanhtml(raw_html)
        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))

    df_minBY = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_minBY.head(30)
    df_minBY = df_minBY[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_append.append(df_minBY, ignore_index=True)

    del df_minBY
except:
    print(minby, 'link is missed')

# ___________________________________________________
try:

    session = requests.Session()
    response = session.get(beltel, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    data = []

    for elem in soup.select('.field-content a'):
        links.append('https://beltelecom.by' + elem.get('href'))

    for link in links:
        if re.search(r'\bnews\b', link) and not (re.search(r'\bgov\.by\b', link)):  # фильтр по тексту новость
            result = requests.get(link, verify=True)
            soup = BeautifulSoup(result.content, 'html.parser')
            card = {}
            card['country'] = 'BY'
            card['provider'] = 'Beltelecom'
            card['title'] = soup.select('.page-title')[0].text.strip()
            try:
                date_clean = datetime.datetime.strptime(soup.select('.node__submitted span')[0].text.strip(),
                                                        '%d.%m.%Y')  # обрабатываем строку для получения даты
                card['date'] = date_clean
            except:
                card['date'] = 'none'
            textrow = soup.select('p')
            raw_html = "".join([str(n) for n in textrow])
            card['news_text'] = cleanhtml(raw_html)
            card['link'] = link
            data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
            print('Ссылка {} была обработана'.format(link))
        else:
            print('это не новость')
    df_beltel = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_beltel.head(30)
    df_beltel = df_beltel[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_append.append(df_beltel, ignore_index=True)

    del df_beltel
except:
    print(beltel, 'link is missed')

# ___________________________________________________
try:

    session = requests.Session()
    response = session.get(becloud, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    data = []

    for elem in soup.select('.news__info a'):
        links.append('https://becloud.by' + elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'BY'
        card['provider'] = 'Becloud'
        card['title'] = soup.select('.h1.h1 span')[0].text.strip()
        date_clean = datetime.datetime.strptime(soup.select('.media__date')[0].text.strip(),
                                                '%d.%m.%Y')  # обрабатываем строку для получения даты
        card['date'] = date_clean
        textrow = soup.select('p')
        raw_html = "".join([str(n) for n in textrow])
        card['news_text'] = cleanhtml(raw_html)
        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))
    df_becloud = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_becloud.head(30)
    df_becloud = df_becloud[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_append.append(df_becloud, ignore_index=True)
    del df_becloud
except:
    print(becloud, 'link is missed')

# ___________________________________________________
try:

    session = requests.Session()
    response = session.get(mts_arm, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    data = []
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  # функция чистит html

    for elem in soup.select('.news-list-item__box-cell a'):
        links.append('https://www.mts.am' + elem.get('href'))

    for link in links:
        if re.search(r'\bnews\b', link):  # фильтр по тексту новость
            session = requests.Session()
            response = session.get(link, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
            soup = BeautifulSoup(response.content, 'html.parser')
            card = {}
            card['country'] = 'Arm'
            card['provider'] = 'MTS'
            card['title'] = soup.select('.section-box__padding h1')[0].text.strip()
            date_clean = datetime.datetime.strptime(re.search('\d{4}/\d\d/\d\d', link)[0],
                                                    '%Y/%m/%d')  # обрабатываем строку для получения даты
            card['date'] = date_clean
            textrow = soup.select('p')
            raw_html = "".join([str(n) for n in textrow])
            card['news_text'] = cleanhtml(raw_html)
            card['link'] = link
            data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
            print('Ссылка {} была обработана'.format(link))
        else:
            print('это не новость')

    df_MTSA = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные

    df_MTSA.head(30)
    df_MTSA = df_MTSA[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_append.append(df_MTSA, ignore_index=True)
    del df_MTSA
except:
    print(mts_arm, 'link is missed')

# _________________________________________________
try:
    session = requests.Session()
    response = session.get(beeline_am, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    data = []

    for elem in soup.select('.grid__item.grid__item--50.ver-top-box a'):
        links.append(elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/98.0.4758.102'}, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'Arm'
        card['provider'] = 'Beeline'

        raw_title = soup.select('.news-wrapper__title.news-wrapper__title--short.fs26')[0].text.strip()
        TOKEN = 'AQVN3FN4EC82RGUBiVtMfVLiVEo971_Ft03Mhbkn'
        headers = {"Authorization": f"Api-Key {TOKEN}", }
        res = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate",
                            json={"targetLanguageCode": 'ru', "texts": raw_title, },
                            headers=headers)
        a = res.json()['translations'][0]
        card['title'] = a['text']
        del a

        date_clean = datetime.datetime.strptime(re.search('\d{4}/\d\d/\d\d', link)[0],
                                                '%Y/%m/%d')  # обрабатываем строку для получения даты
        card['date'] = date_clean

        textrow = soup.select('p')
        raw_html = "".join([str(n) for n in textrow])
        TOKEN = 'AQVN3FN4EC82RGUBiVtMfVLiVEo971_Ft03Mhbkn'
        headers = {"Authorization": f"Api-Key {TOKEN}", }
        res = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate",
                            json={"targetLanguageCode": 'ru', "texts": cleanhtml(raw_html), },
                            headers=headers)
        a = res.json()['translations'][0]
        card['news_text'] = a['text']
        del a

        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))

    df_beeline = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_beeline.head(30)
    df_beeline = df_beeline[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_append.append(df_beeline, ignore_index=True)
    del df_beeline
except:
    print(beeline_am, 'link is missed')
# ___________________________________________________

try:

    session = requests.Session()
    response = session.get(ucom, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)

    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    data = []
    a = int(0)

    for elem in soup.select('.clear-fix.news-inner a'):
        links.append(elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)

        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'Arm'
        card['provider'] = 'Ucom'
        card['title'] = soup.select('.fedra-medium.tu.fs15.news-title')[0].text.strip()
        date_clean = datetime.datetime.strptime(soup.select('.date-txt.fedra-book.fs15')[0].text.strip(),
                                                '%d/%m/%Y')  # обрабатываем строку для получения даты
        card['date'] = date_clean
        textrow = soup.select('p')
        raw_html = "".join([str(n) for n in textrow])
        card['news_text'] = cleanhtml(raw_html)
        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))

    df_ucom = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_ucom.head(30)
    df_ucom = df_ucom[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме
    df_append = df_append.append(df_ucom, ignore_index=True)
    del df_ucom
except:
    print(ucom, 'link is missed')
# ___________________________________________________
try:

    session = requests.Session()
    response = session.get(psrc, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)

    import pandas as pd

    print(response)
    res = str()
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    data = []

    for elem in soup.select('.flex-1.flex.flex-col.news-conent-info a'):
        links.append('https://psrc.am' + elem.get('href'))

    for link in links:
        session = requests.Session()
        response = session.get(link, headers={'User-Agent': 'Google Chrome/96.0.4664.45'}, verify=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        card = {}
        card['country'] = 'Arm'
        card['provider'] = 'psrc'
        raw_title = soup.select('.page-header__title.flex.align-center.subnav__sub_title.lib-sub-title.newsPress')[
            0].text.strip()
        TOKEN = 'AQVN3FN4EC82RGUBiVtMfVLiVEo971_Ft03Mhbkn'
        headers = {"Authorization": f"Api-Key {TOKEN}", }
        res = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate",
                            json={"targetLanguageCode": 'ru', "texts": raw_title, },
                            headers=headers)
        a = res.json()['translations'][0]
        card['title'] = a['text']
        del a

        raw_date = soup.select('.page-header__title')[0].text.strip()
        TOKEN = 'AQVN3FN4EC82RGUBiVtMfVLiVEo971_Ft03Mhbkn'
        headers = {"Authorization": f"Api-Key {TOKEN}", }
        res = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate",
                            json={"targetLanguageCode": 'ru', "texts": raw_date, },
                            headers=headers)
        a = res.json()['translations'][0]
        date_clean = datetime.datetime.strptime(a['text'], '%B %d, %Y')  # обрабатываем строку для получения даты
        card['date'] = date_clean
        del a

        textrow = soup.select('p')
        raw_html = "".join([str(n) for n in textrow])
        TOKEN = 'TOKENsdfjkhlhoewiroi762783648726TOKEN'
        headers = {"Authorization": f"Api-Key {TOKEN}", }
        res = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate",
                            json={"targetLanguageCode": 'ru', "texts": cleanhtml(raw_html), },
                            headers=headers)
        a = res.json()['translations'][0]
        card['news_text'] = a['text']
        del a

        card['link'] = link
        data.append(card)  # приклеиваем словарь элементов в один список. элементы д.б. str
        print('Ссылка {} была обработана'.format(link))

    df_psrc = pd.DataFrame(data).drop_duplicates()  # удаляем дублирующиеся данные
    df_psrc.head(30)
    df_psrc = df_psrc[
        ['country', 'provider', 'date', 'title', 'news_text', 'link']]  # меняем порядок столбцов в датафрейме

    df_append = df_append.append(df_psrc, ignore_index=True)
    del df_psrc

except:
    print('link is missed')

print(df_append)

writer = pd.ExcelWriter('C:\\Users\\Desktop\\all_news.xlsx', engine='xlsxwriter')  # Specify a writer
df_append.to_excel(writer,
                   'df_append')  # Write your DataFrame to a file. Добавить добавление записей в один и тот же файл https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html#pandas.DataFrame.to_excel
writer.save()  # Save the result
writer.close()

df_append = df_append.set_index('date', drop=True)  # убрать дублированный столбец даты, добавить фильтр
df_append = df_append.sort_index(ascending=False)  # (причесать формат дат  новостей по которым  ошибка)
df_append = df_append.query('@beginfrom <= date <= @time')  # рабочий формат 20211127

df_append = df_append.reset_index()
df_append = df_append[['date', 'country', 'provider', 'title', 'link']]

from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

emailfrom = "mailbox@mail.ru"
emailto = "email1@mts.ru, email2@mts.ru"
fileToSend = ["C:\\Users\\Desktop\\all_news.xlsx"]
username = "wmailbox@mail.ru"
password = "slhghahijk,nbv898234"

server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
n = 0

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "week news " + time

html = """\
<html>
  <head></head>
  <body>
    {0}

This is an automatically generated email
Please do not reply

  </body>
</html>
""".format(df_append.to_html(justify='center'))
del df_append

msgText = MIMEText(html, 'html')

for file in fileToSend:
    ctype, encoding = mimetypes.guess_type(fileToSend[n])  # добавить цикл со списком files (for fileToSend in files)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend[n], "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend[n])
    n = +1
    msg.attach(attachment)  # закончить цикл

msg.attach(msgText)

print('send report? y/n')
sendrep = str(input())
if sendrep == 'y':
    # для gmail server.starttls()
    server.login(username, password)
    server.sendmail(emailfrom, emailto.split(","), msg.as_string())
    server.quit()
    print("Сообщение отправлено")
else:
    print("Сообщение не отправлено")