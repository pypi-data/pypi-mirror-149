import requests, xlrd
import re,os,datetime,json
from requests_toolbelt.multipart.encoder import MultipartEncoder

    
industry_excel_path=''
sens_words_path=''
allowed_domains=''
pic_api=''
country_excel_path=''

def xstr(self,s):
    return '' if s is None else str(s).strip()


def pro_industry_dict(self):
    path = self.industry_excel_path
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
                    keys.append(x)
                    values.append(table.row_values(i)[2])
            else:
                keys.append(row_value)
                values.append(table.row_values(i)[2])
        total.append(dict(zip(keys, values)))
        keys = []
        values = []

    return total


def pro_country_dict(self):
    path = self.country_excel_path

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


def pro_sensitive_dict(self,art_content):
    data = xlrd.open_workbook(self.sens_words_path)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    kwd = []
    for i in range(0, nrows):
        kwd.append(table.row_values(i)[0])
    kwd = tuple(kwd)
    return re.sub("|".join(kwd), "***", art_content)


def pro_dict_art(self, art_content):
    if len(art_content.strip()) == 0:
        return ''
    country_dict = self.pro_country_dict()
    country_list = list(country_dict.keys())
    country = [country_dict[country_name] for country_name in country_list if country_name in art_content]
    industry = self.pro_industry_dict()
    zhongyou = list(industry[0].keys())
    yingyou = list(industry[1].keys())
    zhongfei = list(industry[2].keys())
    yingfei = list(industry[3].keys())
    inds_1 = [industry[0][key] for key in zhongyou if key in art_content]
    inds_2 = [industry[1][key] for key in yingyou if key in art_content]
    inds_3 = [industry[2][key] for key in zhongfei if key in art_content]
    inds_4 = [industry[3][key] for key in yingfei if key in art_content]
    inds = inds_1 + inds_2 + inds_3 + inds_4
    inds = list(set(inds))
    country = list(set(country))
    return country, inds


def pic_process(self, art_content, art_url):
    pic_path = '/PIC/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    pic_url = re.findall('src="(.*?)"', art_content, re.S)

    for url in pic_url:
        file = pic_path + '/' + url.split('/')[-1]
        if not os.path.isdir(pic_path):
            os.makedirs(pic_path)
        dnurl = url

        if str(url).startswith('./'):
            dnurl = art_url.replace(art_url.split('/')[-1], '') + url.replace('./', '')
        elif not str(url).startswith('http') or not str(url).startswith('//'):
            dnurl = 'http://' + ''.join(self.allowed_domains) + url
        try:
            r = requests.get(dnurl, timeout=5)
            if r.status_code == 200:
                with open(file, 'wb') as f:
                    f.write(r.content)
            else:
                continue
            pic_api = self.pic_api
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


def filter_tags(self, htmlstr):
    # 先过滤CDATA
    if htmlstr is None or htmlstr == '' or htmlstr == '[]':
        return ''
    htmlstr = ''.join(htmlstr)
    re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)  # 匹配CDATA
    re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>', re.I)  # Script
    re_style = re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>', re.I)  # style
    # re_br = re.compile('<brs*?/?>')  # 处理换行
    re_h = re.compile('(?!</?(sub|br|table|tr|p|span|div|td|img|sup).*?>)<.*?>')
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    # s = re_br.sub('<br>', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    s = s.replace('\t', '').replace('\xa0', '')
    s = s.replace(u'\u3000', u'').replace(u'\xa0', u'')
    return s


def replaceCharEntity(self, htmlstr):
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