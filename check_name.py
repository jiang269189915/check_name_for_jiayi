#encoding:utf-8
import requests
import sys
from random import choice
import json
import time
import os
from urllib import quote

url = "http://yct.sh.gov.cn/namedeclare/check/check_biz"

word_set = set()
record_list1 = []
record_list2 = []

def get_word(record_list):
    i = 0
    while 1:
        word = choice(list(word_set))
        if word not in record_list:
            record_list.append(word)
            return word
        i += 1
        if i == len(word_set) - 1:
            return

def check_name_once(payload, org, ind, ind_code, name):
    combine_name = "上海" + name + ind + org
    payload += "check_nameDistrict=%s&check_nameTrad=%s&check_nameIndDesc=%s&check_industryCode=%s&check_nameForm=%s&check_nameApp=%s"%(quote("上海"),quote(name), quote(ind), ind_code, quote(org), quote(combine_name))
    headers = {
            'cache-control': "no-cache",
            'postman-token': "32c0ca18-f7b0-9d79-3e15-8c13da5ed445",
            'content-type': "application/x-www-form-urlencoded",
            'Host': "yct.sh.gov.cn",
            'Origin': "http://yct.sh.gov.cn",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
            }
    response = requests.request("POST", url, data=payload, headers=headers)
    dict = json.loads(response.text)
    #print response.text
    if dict.get("result", None) == None:
        return False
    return True

def main():
    if len(sys.argv) < 4:
        print "USAGE:python check_name.py 组织形式 行业表述 行业代码"
        exit(1)
    org = sys.argv[1]
    ind = sys.argv[2]
    ind_code = sys.argv[3]
    first_word = ""
    if len(sys.argv) == 5:
        first_word = sys.argv[4]
    init_payload = "self_id=&self_name=&check_items=NAME&check_indPhy=&check_nameRegOrgan=000000&check_nameApoOrgan=000000"
    f = open("word.txt", 'rb')
    for line in f:
        line = line.strip()
        word_set.add(line)
    f.close()
    #print check_name_once(init_payload, org, ind, ind_code, "康德")
    i = 0
    while 1:
        word = get_word(record_list1)
        if first_word != "":
            word = first_word
        word1 = get_word(record_list2)
        if not word or not word1:
            continue
        name = word + word1
        if not check_name_once(init_payload, org, ind, ind_code, name):
            if i == 5:
                i = 0
                print '\t'
            print name,
            i += 1
        time.sleep(1)

if  __name__ == "__main__":
    main()
