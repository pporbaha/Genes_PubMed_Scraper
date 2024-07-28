""" WARNING: 
Webscraping may be illegal. please check your country rules before doing that!!!
__author__ = 'Pedram Porbaha'
__email__ = 'p.porbaha@gmail.com'
__date__ = '2022'
"""

# v1.2 =>doesnt wait for genes with only one article
# because in this results, the only one article opened

import pandas as pd
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from random import randint
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from datetime import datetime
from pedram import check_internet
import os

# %%
data = pd.read_csv(r'Data\protein-coding_gene.txt', sep='\t')

os.makedirs('Result', exist_ok=True)
os.chdir('Result')

driver = webdriver.Chrome(binary_path)
driver.maximize_window()

check_internet()
URL = 'https://pubmed.ncbi.nlm.nih.gov/'
driver.get(URL)


def find(path):
    return driver.find_element('css selector', path)


def finds(path):
    return driver.find_elements('css selector', path)


# %%
def pubmed_search(gene):
    # !!! input your seach query here !!!
    txt = f'({gene}) AND (MDD OR Major depression OR Major depressive disorder OR Depressive disorder, major [MeSH] OR Depressive disorder [MeSH])'

    search_query = quote(txt)
    url = 'https://pubmed.ncbi.nlm.nih.gov/?term='+search_query
    driver.get(url)


def extract_result_number():
    path = "#full-view-heading > h1.heading-title"
    elems = finds(path)
    if elems:  # it means only one result and the article opened directly
        return 1
    else:
        path = ".results-amount-container .results-amount"
        elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(('css selector', path))
        )
        txt = elem.text
        pattern = r'(\d+) results?'
        mo = re.search(pattern, txt)
        if mo:
            number = mo.group(1)
        else:
            number = 0
        return int(number)


def extract_pages_nums():
    path = 'label.of-total-pages'
    elems = finds(path)
    if elems:
        txt = elems[0].text
        pattern = r'of (\d+)'
        mo = re.search(pattern, txt)
        page_nums = int(mo.group(1))
    else:
        page_nums = 1
    return page_nums


def expand_all_pages(idx, gene, max_page_nums=4):

    page_nums = extract_pages_nums()
    if page_nums > max_page_nums:
        error = f"For this gene {page_nums} pages found. {max_page_nums=} is considered"
        write_temp(idx, gene, error)
        page_nums = max_page_nums

    for i in range(1, page_nums):
        path = '#bottom-page-number-input'
        elem = find(path)
        current_page = int(elem.get_attribute('value'))
        # print(f'{current_page=}')

        if current_page == page_nums:
            print(
                f'All {page_nums=} succesfully expanded. We are in {current_page} page')
            break

        path = '#search-results  .search-results-paginator.next-results-paginator> button'
        btns = finds(path)
        if btns:  # because of last page
            btn = btns[0]
        else:
            break
        ActionChains(driver).move_to_element(btn).click().perform()

        tic = datetime.now()
        # new current_page
        while True:
            path = '#bottom-page-number-input'
            # elem = WebDriverWait(driver, 30).until(
            #     EC.presence_of_element_located(('css selector', path))
            # )
            elem = find(path)
            new_current = int(elem.get_attribute('value'))
            # print(f'{new_current=}')
            # becaues if you dont scroll to it, it doesent change!
            ActionChains(driver).move_to_element(elem).perform()
            if new_current != current_page:
                print(f'expanded after {new_current=} successfully')
                break

            # because of last page
            path = '#search-results  .search-results-paginator.next-results-paginator> button'
            btns = finds(path)
            if btns:
                if btns[0].is_enabled():
                    print("Btn in enabled because it cant load. so I click again")
                    btn.click()
            sleep(randint(1, 4))

            toc = datetime.now()
            delta_time = toc - tic
            if delta_time.seconds > 10:  # if it is very long time
                error = 'time consumed is more than 10 seconds to expand all page(maybe last page not fully loded)s'
                write_temp(idx, gene, error)  # idx will be defined in main()
                break


def extract_articles():
    path = '.docsum-title'
    # may be one article load but we dont need genes with less than 2 articles
    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(('css selector', path))
    )
    elems = finds(path)
    links = []
    for elem in elems:
        links.append((elem.text, elem.get_attribute('href')))
    return links

def extract_one_article():
    path = '#full-view-heading > h1'
    elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(('css selector', path))
    )
    links = []
    links.append((elem.text, driver.current_url))
    return links

# %%
sep = '\t|\t'


def write_initial():
    with open('counts.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write('idx'+'\t'+'Symbol'+'\t'+'ArticleCounts')
        f.write('\n')

    with open('links.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write('idx'+sep+'Symbol'+sep+'Count'+sep+'Article Title'+'\t' +
                'Article Link'+sep+'and so on...')
        f.write('\n')
    with open('temp.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write('idx'+'\t'+'Gene'+'\t')
        f.write('\n')
    with open('genes_with_zero_result.txt', 'w',
              encoding='utf-8', errors='ignore') as f:
        f.write('idx'+'\t'+'Gene'+'\t')
        f.write('\n')
    with open('genes_with_only_one_result.txt', 'w',
              encoding='utf-8', errors='ignore') as f:
        f.write('idx'+'\t'+'Gene'+'\t')
        f.write('\n')


def write_counts(idx, gene, count):
    with open('counts.txt', 'a', encoding='utf-8', errors='ignore') as f:
        f.write(str(idx)+'\t'+gene+'\t'+str(count))
        f.write('\n')


def write_links(idx, gene, count, links):
    with open('links.txt', 'a', encoding='utf-8', errors='ignore') as f:
        f.write(str(idx)+sep+gene+sep)
        f.write(str(count)+sep)
        for title, link in links:
            f.write(title + '\t')
            f.write(link+sep)
        f.write('\n')


def write_genes_with_zero_result(idx, gene):
    with open('genes_with_zero_result.txt', 'a',
              encoding='utf-8', errors='ignore') as f:
        f.write(str(idx)+'\t' + gene)
        f.write('\n')


def write_genes_with_only_one_result(idx, gene):
    with open('genes_with_only_one_result.txt', 'a',
              encoding='utf-8', errors='ignore') as f:
        f.write(str(idx)+'\t' + gene)
        f.write('\n')


def write_temp(idx, gene, error):
    with open('temp.txt', 'a', encoding='utf-8', errors='ignore') as f:
        f.write(str(idx)+'\t'+gene+'\t'+str(error))
        f.write('\n')


def write_current_position(idx, gene, begin, end):
    with open('current_position.txt', 'w', encoding='utf-8', errors='ignore') as f:
        f.write(str(idx)+'\n')
        f.write('I extracted until:\n')
        f.write(str(idx)+'\t'+gene+'\n')
        f.write(f'Schedule was from {begin=} to {end=}')

def read_current_position():
    with open('current_position.txt', encoding='utf-8') as f:
        lines = f.readlines()
        position = int(lines[0].strip())
    return position
    

def estimate_finished_time(time_start, counts, idx, begin=0):
    time_now = datetime.now()
    timeConsumedAverage = (time_now-time_start) / (idx - begin + 1)  # because idx begins from 0
    finishEstimatedTime = time_now + timeConsumedAverage*(counts-idx)

    return finishEstimatedTime.strftime("%D:%H:%M:%S")
# %%


def main():
    
    user = input('Do you want to create new result files? (enter y for yes and N for continue from last item)\n')
    if user in ['y', 'Y']:
        write_initial()
        begin = 0
    else:
        begin = read_current_position()

    gene_counts = len(data['symbol'][begin:])
    all_genes = len(data['symbol'])
    time_start = datetime.now()

    for idx, gene in enumerate(data['symbol'][begin:], begin):
        try:
            finish_time = estimate_finished_time(time_start, all_genes, idx, begin)
            print(f'{gene=}, {idx=} from all {all_genes} ,{finish_time=}')
            write_current_position(idx, gene, begin, 'end')
            check_internet()
            pubmed_search(gene)
            count = extract_result_number()
            if count == 0:
                write_genes_with_zero_result(idx, gene)
            elif count == 1:
                links = extract_one_article()
                write_genes_with_only_one_result(idx, gene)
                write_counts(idx, gene, count)
                write_links(idx, gene, count, links)
            else:
                expand_all_pages(idx, gene)
                links = extract_articles()
                write_counts(idx, gene, count)
                write_links(idx, gene, count, links)

        except Exception as e:
            error = str(e)
            print(f'>>Error occurred in {gene} because of {error}')
            write_temp(idx, gene, error.replace('\n', ' '))

        sleep(1)


if __name__ == '__main__':
    main()
