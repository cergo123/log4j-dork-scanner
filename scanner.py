import urllib
import requests
import re
from bs4 import BeautifulSoup
import subprocess
import argparse


parser = argparse.ArgumentParser(description='Log4J auto scanner')
parser.add_argument('-d', '--dork', type=str,  dest='dork',
                    help='The dork to search in google', required=True)
parser.add_argument('-n', '--no_of_pages', type=int,  dest='no_of_pages',
                    help='Number of pages in google results', required=True)
args = vars(parser.parse_args())


def scrap(query, no_of_pages, url=None):
    # desktop user-agent
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    mobile_user_agent = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, " \
                        "like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36 "

    query = query.replace(' ', '+')
    if url is None:
        url = f"https://google.com/search?q={query}"

    headers = {"user-agent": user_agent}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='g'):
            link = g.find('a')['href']
            if link and is_url(link):
                results.append(link)
        no_of_pages = no_of_pages-1
        if no_of_pages <= 0:
            return results
        else:
            if soup.find(id='pnnext'):
                new_url = 'https://google.com' + str(soup.find(id='pnnext')['href'])
                return results + scrap(query=query, no_of_pages=no_of_pages, url=new_url)
            else:
                return results

    else:
        print('ERROR', resp.status_code)
        return []


def is_url(x):
    return bool(re.match(
        r"(https?|ftp)://" # protocol
        r"(\w+(\-\w+)*\.)?" # host (optional)
        r"((\w+(\-\w+)*)\.(\w+))" # domain
        r"(\.\w+)*" # top-level domain (optional, can have > 1)
        r"([\w\-\._\~/]*)*(?<!\.)" # path, params, anchors, etc. (optional)
    , x))


def save(results):
    # clear the urls
    file = open("urls.txt", "r+")
    file.truncate(0)
    file.close()

    # append new results
    with open('urls.txt', 'a') as the_file:
        for result in results:
            the_file.write(f"{result}\n")


if __name__ == '__main__':
    print(f'Initialization => [dork: {args["dork"]} - number of pages: {args["no_of_pages"]}]')
    print('scrapping...')
    results = scrap(query=args['dork'], no_of_pages=args['no_of_pages'])
    print(f'{len(results)} links have been scrapped')
    save(results)
    print('scanning...')
    subprocess.call('python log4j-scan.py -l urls.txt --run-all-tests --waf-bypass ', shell=True)
