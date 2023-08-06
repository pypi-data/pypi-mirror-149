import requests, xlrd,urllib
import re, os, datetime, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from lxml import etree
from translate import Translator
import http.client
import hashlib,jieba
import random,pymysql


# class ruinews():
#     def __init__(self):
pic_api = ''
upload_api = ''
rt = ''
TIMEOUT = 10
db=''
cursor=''

def mysql_conn(ip,user,pwd,db_name):
    db = pymysql.connect(ip, user, pwd, db_name)
    cursor = db.cursor()
    return db,cursor

def insert_db(product_info,tb_name):
    values = ', '.join(['%s'] * len(product_info))
    fields = product_info.keys()
    try:
        qry = 'Insert Into '+ tb_name +' (%s) Values (%s);' % (','.join(fields), values)

        cursor.execute(qry, [product_info[x] for x in fields])
        db.commit()

    except Exception as e:
        print(f'入库失败，原因:{str(e)}')
        db.rollback()

def xstr(s):
    return '' if s is None else str(s).strip()

def get_request(url,hds,charset='utf-8'):

    r=requests.get(url,headers=hds,timeout=TIMEOUT)
    text=r.content.decode(charset)
    r.close()
    return etree.HTML(text)

def get_api_content(url,hds,charset='utf-8'):
    r=requests.get(url,headers=hds)
    text=r.content.decode(charset)
    r.close()
    html=json.loads(text)
    # html = xmltodict.parse(text)
    # jsont=json.dumps(html)
    # html=json.loads(jsont)
    return html
def post_request(url,data,hds,charset='utf-8'):
    r=requests.post(url,headers=hds,data=data)
    text=r.content.decode(charset)
    r.close()
    html=json.loads(text)
    return html
def get_url_html(url,charset='utf-8'):
    s = requests.session()
    s.keep_alive = False
    s.proxies = None
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
    }
    s.headers = headers
    r = s.get(url)

    if r.status_code==200:
        html = r.content.decode(encoding=charset, errors='ignore')
    else:
        html=''
    return html

def element_convert(s):
    #xpath取到的element转换为html
    s = etree.tostring(s, pretty_print=True, method='html', encoding='utf-8')
    s = str(s, encoding="utf-8")
    return s
def stamp_convent(timeStamp):
    """
    时间戳转换格式
    """
    dateArray = datetime.datetime.fromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return otherStyleTime

def download_file(_dnurl,_filename):
    """
    下载文件,filename全路径
    """
    _dir=_filename.replace(_filename.split('/')[-1],'')

    if os.path.exists(_filename):
        print('文件已存在%s'%_filename)
        return
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    r = requests.get(_dnurl)
    fo = open(_filename,'wb')
    fo.write(r.content)
    fo.close()
    print("Sucessful to download" + " " + _filename)
def getFile(url,file_name):
    # file_name = url.split('/')[-1]
    try:
        u = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
       #碰到了匹配但不存在的文件时，提示并返回
        print(url, "url file not found")
        return
    block_sz = 8192
    with open(file_name, 'wb') as f:
        while True:
            buffer = u.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break

    print ("Sucessful to download" + " " + file_name)
def trans_word(text,from_lan,to_lan):
    if len(text)==0 or text is None:
        return
    translator= Translator(to_lang=to_lan,from_lang=from_lan)
    temp = translator.translate(text)
    return temp


def pro_industry_dict():
    #取出xuci表中所有词生成dict
    path =rt+'xuci.xlsx'
    if not os.path.exists(path):
        print('ERR：行业文件不存在')
        return
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    keys = []
    values = []
    total = []

    for column_index in range(2, 6):
        for i in range(1, nrows):
            row_value = table.row_values(i)[column_index].strip()
            if len(row_value) == 0:
                continue
            if ';' in row_value:
                for x in row_value.split(';'):
                    if column_index ==3 or column_index ==5:
                        keys.append(x+' ')
                    else:
                        keys.append(x)
                    values.append(table.row_values(i)[2])
            else:
                if column_index ==3 or column_index ==5:
                    keys.append(row_value+' ')
                else:
                    keys.append(row_value)
                values.append(table.row_values(i)[2])
        total.append(dict(zip(keys, values)))
        keys = []
        values = []

    return total


def pro_country_dict():

    path =rt+'country.xls'
    if not os.path.exists(path):
        print('ERR：国家字典文件不存在')
        return
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    keys1 = [table.row_values(i)[0] for i in range(1, nrows)]
    keys2 = [table.row_values(i)[2] for i in range(1, nrows)]
    values = [table.row_values(i)[1] for i in range(1, nrows)]

    c = dict(zip(keys1, values))
    c2 = dict(zip(keys2, values))
    c.update(c2)
    return c


def pro_sensitive_dict(art_content):
    path=rt+'sensitive.xlsx'
    if not os.path.exists(path):
        print('ERR：敏感词字典不存在')
        return
    data = xlrd.open_workbook(path)

    table = data.sheet_by_index(0)
    nrows = table.nrows
    kwd = []
    for i in range(0, nrows):
        kwd.append(table.row_values(i)[0])
    kwd = tuple(kwd)
    return re.sub("|".join(kwd), "***", art_content)
CN_NUM = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,'十': 10,
        '十一': 11, '十二': 12
}
def timestamp_datetime(ts):
    '''
    timestamp转datetime格式
    :param ts:
    :return:
    '''
    if isinstance(ts, (int, float, str)):
        try:
            ts = int(ts)
        except ValueError:
            raise

        if len(str(ts)) == 13:
            ts = int(ts / 1000)
        if len(str(ts)) != 10:
            raise ValueError
        else:
            raise ValueError()

    return datetime.datetime.fromtimestamp(ts)
def pro_art_date(art_date:str):
    if art_date=='' or art_date is None:
        return False
    art_date=art_date.replace(' - ','-').strip()
    art_date=art_date.replace('年','-').replace('月','-').replace('日','')
    if len(art_date)>30:
        return False
    if art_date.find('T')>0:
        art_date=art_date[0:art_date.rfind('-')].replace('T', ' ')
    # for month in CN_NUM:
    #     if month in art_date:
    #         art_date = art_date.replace(month, str(CN_NUM[month]))

    if len(art_date) <= 19 and len(art_date)>16:
        ft = '%Y-%m-%d %H:%M:%S'
    elif len(art_date) == 16:
        ft = '%Y-%m-%d %H:%M'
    elif len(art_date) < 8:
        return False
    else:
        ft = '%Y-%m-%d'

    try:
        t1 = datetime.datetime.strptime(art_date, ft)
        t = datetime.datetime.now()
        t = datetime.datetime.strftime(t, '%Y-%m-%d')

        if str(t1)[0:10]==str(t)[0:10]:
            return True
        else:
            return False
    except:
        return False

def pro_dict_art(art_content,art_title):
    if len(art_content.strip()) == 0:
        return ''
    art_content = re.sub(r'<(.*?)>', '', art_content)
    art_split = jieba.lcut(art_content)

    country_dict = pro_country_dict()
    country_list = list(country_dict.keys())
    country = [country_dict[country_name] for country_name in country_list if country_name in art_title]
    if len(country) == 0:
        country = [country_dict[country_name] for country_name in country_list if country_name in art_split]
    industry = pro_industry_dict()
    zhongyou = list(industry[0].keys())
    yingyou = list(industry[1].keys())
    zhongfei = list(industry[2].keys())
    yingfei = list(industry[3].keys())
    inds_1 = [industry[0][key] for key in zhongyou if key in art_split]
    inds_2 = [industry[1][key] for key in yingyou if key in art_split]
    inds_3 = [industry[2][key] for key in zhongfei if key in art_split]
    inds_4 = [industry[3][key] for key in yingfei if key in art_split]
    inds = inds_1 + inds_2 + inds_3 + inds_4
    inds = list(set(inds))
    country = list(set(country))
    return country, inds


def pic_process(art_content, art_url,domain_url=''):
    pic_path =datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    pic_url = re.findall('src="(.*?)"', art_content, re.S)
    if domain_url=='':
        domain_url=art_url[0:art_url.find('/',art_url.find('://')+3)]

# //data:image
    for url in pic_url:
        pic_name=url.split('/')[-1]
        file = pic_path + '/' + url.split('/')[-1]
        if url.startswith('data:image') and art_content.find('data-src=')>0:
            art_content = art_content.replace(url, '')
            art_content = art_content.replace('data-src=', '><img src=')
            continue
        if pic_name.find('.')==-1:
            art_content= art_content.replace(url,'')
            continue
        if not os.path.isdir(pic_path):
            os.makedirs(pic_path)
        dnurl = url

        if str(url).startswith('./'):
            dnurl = art_url.replace(art_url.split('/')[-1], '') + url.replace('./', '')
        elif not str(url).startswith('http') :
            dnurl = domain_url + url
        try:
            r = requests.get(dnurl, timeout=5)
            if r.status_code == 200:
                with open(file, 'wb') as f:
                    f.write(r.content)
            else:
                continue

            m = MultipartEncoder(
                fields={'file': (url.split('/')[-1], open(file, 'rb'))}
            )
            headers = {'Content-Type': m.content_type}

            r = requests.post(pic_api, data=m.read(), headers=headers)

            if r.status_code == 200:
                r = r.text
                new_img_url = json.loads(r)['url']
                art_content = art_content.replace(url, new_img_url)
                os.remove(file)
            else:
                print('ERR:文件上传接口出错,返回状态码%s' % r.status_code)

        except Exception as e:
            continue

    return art_content

def del_tags(html,tag):
    #去除指定标签
    if html is None or len(html)==0:
        return ''
    if len(tag)==0:
        return html
    re_tag = re.sub(r'<%s' % tag + '(.*?)' + '</%s>' % tag, '', html)
    return re_tag
def filter_tags(htmlstr):
    # 先过滤CDATA
    if htmlstr is None or htmlstr == '' or htmlstr == '[]':
        return ''
    htmlstr = ''.join(htmlstr)
    re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)  # 匹配CDATA
    re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>', re.I)  # Script
    re_style = re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>', re.I)  # style
    re_br = re.compile('<br*?/?>')  # 处理换行
    re_h = re.compile('(?!</?(sub|br|table|tr|p|span|div|td|img|sup|strong|h3|h4|h2|b|ul|li|dl|dt).*?>)<.*?>')
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('<br>', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    s = s.replace('\t', '')
    s = s.replace(u'\u3000', u'').replace(u'\xa0', u' ').replace('\u2003','')
    s=re.sub(r'<a(.*?)>','',s)
    s = s.replace('\r\n', '<br>')
    s=s.replace('</a>','').replace('\n', '').replace('\r','')
    return s


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr

def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        for i in s:
            unicodedata.numeric(i)  # 把一个表示数字的字符串转换为浮点数返回的函数
            # return True
        return True
    except (TypeError, ValueError):
        pass
    return False

def get_email(s, au_split):
    sups = []
    slist = s.split(au_split)
    for s in slist:
        pat = re.compile('^(\w*|\d*)@\w*.(com|cn)$', re.S)
        result = ''.join(pat.findall(s))
        if len(result) > 0:
            sups.append(result)
    rtn = ';'.join(sups)
    return rtn

def get_sups(authors, au_split):
    sups = []
    au_split=au_split.replace('，',', ')

    slist = authors.split(au_split)
    for s in slist:

        if s.find('<sup>') > 0 :
            pat = re.compile('<sup>' + '(.*?)' + '</sup', re.S)
            result = ','.join(pat.findall(s))
            if len(result) > 0 :
                sups.append(result)

    rtn = ';'.join(sups)
    return rtn

def str_between(s,s_front,s_end):
    s_list=[]
    pat = re.compile(s_front + '(.*?)' + s_end, re.S)
    result = ''.join(pat.findall(s)).strip()
    s_list.append(result)
    return s_list

def get_string(s, s_split, s_front, s_end,is_split=0):
    sups = []
    slist = s.split(s_split)
    for s in slist:
        # if s.find('<sup>') > 0:
        pat = re.compile(s_front + '(.*?)' + s_end, re.S)
        result = ','.join(pat.findall(s)).strip()
        sups.append(result)
    if is_split==0:
        rtn = ';'.join(sups)
    else:
        rtn = ''.join(sups)
    return rtn


def transAPI1(q):
    if q=='' or q==None or len(q)==0:
        return ''
    translator=Translator(to_lang='zh',from_lang='en')
    art_date=translator.translate(q).replace('年', '-').replace('月', '-').replace('日', '')
    #第三方库有限制
    return art_date.replace(' ','')
def transAPI(q):
    appid = '20210125000680783'
    secretKey = 'kBG1C0TMC9rBwYwpsNBY'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'  # 原文语种
    toLang = 'zh'  # 译文语种
    salt = random.randint(32768, 65536)
    # q = '1st December 2020'
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)['trans_result'][0]['dst']

        return result

    except Exception as e:
        print(e)
        return ''
    finally:
        if httpClient:
            httpClient.close()

def transAPI_lan(q,from_lan,to_lan):
    appid = '20210125000680783'
    secretKey = 'kBG1C0TMC9rBwYwpsNBY'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = from_lan  # 原文语种
    toLang = to_lan  # 译文语种
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)['trans_result'][0]['dst']

        return result

    except Exception as e:
        print(e)
        return ''
    finally:
        if httpClient:
            httpClient.close()

from gne import GeneralNewsExtractor,ListPageExtractor
import pandas as pd

def check_url(url:str):
    '''
    查重url并写入history.csv文件中
    :return:
    '''
    csv = 'history.csv'
    #文件不存在创建，存在取前100条数据查重
    if os.path.exists(csv):
        df_csv = pd.read_csv(csv).tail(100)
    else:
        df_csv = pd.DataFrame(columns=['url'])
    df_csv.set_index('url')
    csv_ls = []
    #判断csv文件是否存在
    rtn=False
    if df_csv[df_csv['url'].isin([url])].empty:
        if url not in csv_ls:
            csv_ls.append(url)
            rtn=True
    if len(csv_ls) > 0:
        dfb = pd.DataFrame(csv_ls, columns=['url'])
        if df_csv.empty:
            dfb.to_csv(csv)
        else:
            dfb.to_csv(csv, mode='a', header=False)
    return rtn
class ruinewsV2():
    hd = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36',
        # 'Content-Type':'Content-Type: application/json;charset=UTF-8',
    }
    CATALOG={'政策法规':'VlbJTOIFFn','热点新闻': '9m5c5HCKEQ','商业资讯':'UL_ZcKVfOF','农业会展':'binfld-yuY' }
    KWDS=['农业','食品','粮食','农副产品','农产品','肉类','水果','大豆','冷鲜','大蒜','农机','西红柿','土豆','菜类']
    def __init__(self,domain_url,catalogName,web_code='utf-8'):
        self.domain_url=domain_url
        self.web_code=web_code
        self.catalogName=catalogName

    def filter_json_url(self,news_ls):
        #查重json返回的url
        if len(news_ls) == 0:
            print('no data')
            return []
        csv = 'history.csv'
        if os.path.exists(csv):
            df_csv = pd.read_csv(csv).tail(100)
        else:
            df_csv = pd.DataFrame(columns=['url'])
        df_csv.set_index('url')
        csv_ls = []
        for item in news_ls:
            url = item['url']
            if not url.startswith('http'):
                if url.startswith('/'):
                    url = self.domain_url + url
                elif url.startswith('./'):
                    url = self.domain_url + url[1:]
                else:
                    url = self.domain_url + '/' + url
            if df_csv[df_csv['url'].isin([url])].empty:
                if url not in csv_ls:
                    csv_ls.append(url)

        if len(csv_ls) > 0:
            dfb = pd.DataFrame(csv_ls, columns=['url'])
            if df_csv.empty:
                dfb.to_csv(csv)
            else:
                dfb.to_csv(csv, mode='a', header=False)
            return csv_ls
        else:
            return []
    def get_news_list(self,url,links_xpath,is_etree=False):
        #get list方式 返回列表
        r = requests.get(url, headers=self.hd, verify=False)
        html = r.content.decode(self.web_code)
        if is_etree==True:
            html=etree.HTML(html)
            news_ls=html.xpath(links_xpath)
        else:
            ls_ex = ListPageExtractor()
            news_ls = ls_ex.extract(html, feature=links_xpath)

        if len(news_ls) == 0:
            print('no data')
            return []
        csv = 'history.csv'
        if os.path.exists(csv):
            df_csv = pd.read_csv(csv).tail(100)
        else:
            df_csv = pd.DataFrame(columns=['url'])
        df_csv.set_index('url')
        csv_ls = []
        for item in news_ls:
            if is_etree==True:
                url=item
            else:
                url = item['url']
            if not url.startswith('http'):
                if url.startswith('/'):
                    url = self.domain_url + url
                elif url.startswith('./'):
                    url = self.domain_url + url[1:]
                else:
                    url = self.domain_url + '/' + url
            if df_csv[df_csv['url'].isin([url])].empty:
                if url not in csv_ls:
                    csv_ls.append(url)

        if len(csv_ls) > 0:
            dfb = pd.DataFrame(csv_ls, columns=['url'])
            if df_csv.empty:
                dfb.to_csv(csv)
            else:
                dfb.to_csv(csv, mode='a', header=False)
            return csv_ls
        else:
            return []
    def get_news_detail(self,url,content_xpath='',is_kwd=False,
                title_xpath='',test_flag=False,proc_art_date='',
                author_xpath='',no_gne_content=True,
                source_xpath='',IS_EN_SITE=False,
                publish_time_xpath='',web_code=''):

        if not url.startswith('http'):

            if url.startswith('/'):
                url = self.domain_url + url
            elif url.startswith('./'):
                url=self.domain_url+url[1:]
            else:
                url = self.domain_url + '/' + url

        art_ex = GeneralNewsExtractor()
        r=requests.get(url, headers=self.hd, verify=False)
        if r.status_code!=200:
            print('request error')
            return
        if web_code:
            art_html = r.content.decode(web_code)
        else:
            art_html = r.content.decode(self.web_code)
        etree_html=etree.HTML(art_html)
        art_html = re.sub(r' style="' + '(.*?)' + '">', '>', art_html)
        try:
            rst = art_ex.extract(art_html, title_xpath=title_xpath,publish_time_xpath=publish_time_xpath,
                                 body_xpath=content_xpath, with_body_html=True,source_xpath=source_xpath,author_xpath=author_xpath)
        except:
            print('GNE解析出错')
            return
        if proc_art_date != '':
            art_date = etree_html.xpath(publish_time_xpath)[0]
            art_date = eval(proc_art_date)
            rst['publish_time'] = art_date.strip()
        if IS_EN_SITE == True:
            art_date = transAPI(rst['publish_time'])
        else:
            art_date = rst['publish_time']
        if 'T' in art_date:
            art_date = art_date[0:art_date.find('T')]
        flag = pro_art_date(art_date)
        art_date = art_date.replace('年', '-').replace('月', '-').replace('日', '')

        if not flag and not test_flag:
            print('日期非今天%s' % art_date)
            return
        art_title = rst['title']
        if no_gne_content==True:
            etree_html=etree.HTML(art_html)
            if content_xpath!='':
                art_content = element_convert(etree_html.xpath(content_xpath)[0])
            else:
                art_content = rst['body_html']
        else:
            art_content = rst['body_html']
        if art_title == '' or art_content == '':
            print('title or content is empty')
            return
        no_kwd=False
        if is_kwd:
            for kwd in self.KWDS:
                if kwd  in art_title or kwd  in art_content:
                    no_kwd=True
                    break
            if no_kwd==False:
                print('art no kwd')
                return
        art_author = rst['author']
        art_source = rst['source']
        catalogId = self.CATALOG[self.catalogName]
        catalogName = self.catalogName
        art_url = url
        art_content = filter_tags(art_content)
        country = ''
        inds=''
        if not test_flag:
            rtn_dict = pro_dict_art(art_content, art_title)
            country = rtn_dict[0]
            inds = rtn_dict[1]
            art_content = pic_process(art_content, art_url,self.domain_url)
            art_content = pro_sensitive_dict(art_content)
        art_content=re.sub(r' style="'+'(.*?)'+'">','>',art_content)
        nitem = {}
        nitem['country'] = country
        nitem['industry'] = inds
        nitem['catalogId'] = catalogId
        nitem['catalogName'] = catalogName
        nitem['title'] = art_title
        nitem['html'] = art_content
        nitem['source'] = art_source
        nitem['url'] = art_url
        nitem['author'] = art_author
        nitem['releaseAt'] = art_date

        return nitem