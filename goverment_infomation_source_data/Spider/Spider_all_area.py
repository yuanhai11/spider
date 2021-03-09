# *_*coding:utf-8 *_*

import re
import requests
import time
import json
import pymysql

'''
建立数据表信息：
字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期    spider调度时间 
注意：请求一页都返回三页数据

每天请求一次，足够满足需求，根据每天的日期将每天更新的数据（附件链接）保存在数据库
'''

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}

rq = str(time.strftime("%Y%m%d"))
rq_ = str(time.strftime("%Y-%m-%d"))
year = str(time.strftime("%Y"))
month = str(time.strftime("%m"))
day = str(time.strftime("%d"))

print(rq)

# def getxm(txt):
#     lists = ['浙江省科技型中小企业','省重点研发计划项目','省级重点实验室','省级研发中心','大学生创业无偿资助','浙江省科技型中小企业','“雏鹰计划”','杭州市级高新技术企业','市级科技企业孵化器','市众创空间','“1211”计划','“百千万”高技能领军人才','大学生创业企业经营场地补贴','大学生创业无偿资助','浙江省科技型中小企业','“雏鹰计划”','“513武林英才”','“258”人才','国家高新技术企业','众创空间','技术先进型服务企业','省重点研发计划项目','“百人计划”','','','','',]
#
#     xx = ''
#     return xx

conn = pymysql.connect(host='192.168.2.222', user='root', password='123456', database='test', port=3306)
cursor = conn.cursor()
sql = """insert into high_technolory_all_data(id,qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time)values(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"""

#       浙江省省科技厅        http://kjt.zj.gov.cn/col/col1228971341/index.html
def skjt():

    qy = '浙江省'
    ly = '省科技厅'
    url = 'http://kjt.zj.gov.cn/col/col1228971341/index.html'
    # 请求一页返回三页的数据
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall('<li>.*?<a href="(.*?)" title="(.*?)" target="_blank">.*?</a>.*?<span>(.*?)</span></li> ',aaa,re.S)

    for li in lists:
        if '.pdf' == li[0][-4:]:
            continue
        # print(li)
        wylj = 'http://kjt.zj.gov.cn' + li[0]
        bt = li[1]
        fbrq = li[2]
        # 字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期    spider调度时间     (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                try:
                    fbrq = re.findall('class="fbrq">发布日期：(.*?)</span>', nr, re.S)[0]
                except:
                    pass
                fjdz = ''
                fjdzs = re.findall('href="/module/download(.*?)"', nr, re.S)
                if fjdzs != []:
                    for i in fjdzs:
                        fjdz =fjdz + 'http://kjt.zj.gov.cn/module/download'+i+'\n'
                else:
                    fjdz = fjdz +'未解析出附件地址'

                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                print(bt)
                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       杭州人社局        http://hrss.hangzhou.gov.cn/col/col1587845/index.html
def hzrs():
    qy = '杭州市'
    ly = '人社局'
    url = 'http://hrss.hangzhou.gov.cn/col/col1587845/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall('<li><b>·</b>.*?<a href="(.*?)" target="_blank" title="(.*?)">.*?</a><i>(.*?)</i></li>]]></record>',aaa,re.S)
    print(lists)
    exit()
    for li in lists:
        if '.pdf' == li[0][-4:]:
            continue
        # print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://hrss.hangzhou.gov.cn/art/2020/3/4/art_1587845_42074587.html'
            li[0]='http://hrss.hangzhou.gov.cn'+li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)


        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                try:
                    fbrq = '2'+re.findall('<!--信息标题--><div class="subtitle"></div></h3><i>.*?\d(.*?)</i></div>', nr, re.S)[0]
                except:
                    pass
                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))" ', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@'  in i:
                            continue
                        if 'http' not in i:
                            i = 'http://hrss.hangzhou.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                        print(i)
                else:
                    fjdz = fjdz +'未解析出附件地址'
                # print(fjdz)
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       杭州科技局        1.http://kj.hangzhou.gov.cn/col/col1694003/index.html 2.http://kj.hangzhou.gov.cn/col/col1693961/index.html 3.http://kj.hangzhou.gov.cn/col/col1693962/index.html 4.http://kj.hangzhou.gov.cn/col/col1693977/index.html
def hzkj():
    qy = '杭州市'
    ly = '科技局'
    urls = ['http://kj.hangzhou.gov.cn/col/col1694003/index.html'
        ,'http://kj.hangzhou.gov.cn/col/col1693961/index.html',
            'http://kj.hangzhou.gov.cn/col/col1693962/index.html',
            'http://kj.hangzhou.gov.cn/col/col1693977/index.html']

    for i in urls:
        aaa = requests.get(url=i, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
        lists = re.findall('<a href="/art(.*?)" target="_blank" title="(.*?)">.*?</a>.*?<span style=".*?">(.*?)</span>.*?</li>.*?]]></record>.*?<record>',aaa,re.S)
        # print(lists)
        for li in lists:
            if '.pdf' == li[0][-4:]:
                continue
        #     print(li)
            li = list(li)
            if 'http' not in li[0]:
                'http://kj.hangzhou.gov.cn/art/2019/12/2/art_1694003_40717767.html'
                li[0]='http://kj.hangzhou.gov.cn/art'+li[0]
            wylj = li[0]
            bt = li[1]
            fbrq = li[2].strip()
            # print(bt)
            # print(wylj)
            # print(fbrq)

    #
            if fbrq == rq_:
                print(bt)
                print(wylj)
                print(fbrq)
                try:
                    # print(nr)
                    nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                    # print(nr)
                    # 'href="/attach/-1/2001091448071436013.docx"'
                    # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                    try:
                        fbrq = re.findall('发布日期：(.*?)</span>', nr, re.S)[0]
                    except:
                        pass
                    # print(fbrq)
                    fjdz = ''
                    # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                    fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                    ''
                    # '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                    # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                    if fjdzs != []:
                        for i in fjdzs:
                            if '@'  in i:
                                continue
                            if 'http' not in i:
                                i = 'http://kj.hangzhou.gov.cn' + i
                            fjdz =fjdz +i+'\n'
                    else:
                        fjdz = fjdz +'未解析出附件地址'
                    print(fjdz)
        #         #
                    qy = qy
                    ly = ly
                    # xm = getxm(nr)
                    bt = bt
                    nr = nr
                    fjdz = fjdz
                    wylj = wylj
                    fbrq = fbrq
                    spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    # print(spider_time)
            #         print(bt)
            #         print(wylj)
            #         print(fjdz)
            #
                    cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                    conn.commit()
                except:
                    pass

        time.sleep(2)
        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       上城区总        http://search.zj.gov.cn/jrobotfront/search.do?websiteid=330102000000000&searchid=3&pg=&p=1&tpl=174&serviceType=&q=&pq=&oq=&eq=&pos=&begin=&end=
def scrskj():
    import urllib.parse


    # aaa = urllib.parse.unquote(aaa)
    # print(aaa)
    qy = '上城区'
    ly = '政府'
    url = 'http://search.zj.gov.cn/jrobotfront/interfaces/cateSearch.do'
    data = {
    'websiteid': '330102000000000',
    'p': '1',
    'pg': '20',
    'cateid': '167',
    'tpl': '174',
    }
    aaa = eval(requests.post(url=url, headers=headers,data=data).text)['result']
    # print(aaa)
    # ).replace('\\t', '').replace('\\r', '').replace('\\n', '').strip()
    for i in aaa:
        try:
            i = urllib.parse.unquote(i)
            i = str(i).replace('\\t', '').replace('\\r', '').replace('\\n', '').replace(' ', '').strip()
            # print(i)
            wylj,bt =re.findall('<divclass="jcse-news-title"><aclass="mqy_click_button"mqy_name="search_list"target="_blank"href="visit/link\.do\?url=(.*?)&.*?">(.*?)</a></div>',i,re.S)[0]
            # wylj,bt =re.findall('mqy_name="search_list " target="_blank " href="(.*?)">(.*?)</a>',i,re.S)[0]
            bt = str(bt).replace('&nbsp','').strip()
            fbrq =re.findall('日期.<.*?>(.*?)<',i,re.S)[0]
            'http://www.hzsc.gov.cn/art/2020/4/2/art_1497142_42464340.html'
            # print(wylj)
            # print(bt)
            # print(fbrq)
            bt = str(bt).strip()
            fbrq = str(fbrq).strip()
            wylj = str(wylj).strip()

            if fbrq.split(' ')[0] == rq_:
                print(bt)
                print(wylj)
                print(fbrq)
                try:
                    # nr = requests.get(url='http://www.hzsc.gov.cn/art/2019/7/30/art_1267801_36196407.html', headers=headers).text.encode('latin-1').decode('utf8')
                    nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                    # print(nr)

                    fjdz = ''
                    fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                    if fjdzs != []:
                        for i in fjdzs:
                            if '@'  in i:
                                continue
                            if 'http' not in i:
                                i = 'http://hrss.hangzhou.gov.cn' + i
                            fjdz =fjdz +i+'\n'
                    else:
                        fjdz = fjdz +'未解析出附件地址'
                    #
                    try:
                        ly = re.findall('<div class="sub_tit">.*?来源：(.*?)\xa0发布时间.*?<script',nr,re.S)[0]
                    except:
                        ly = '政府'
                    qy = qy
                    ly = ly
                    bt = bt
                    nr = nr
                    fjdz = fjdz
                    wylj = wylj
                    fbrq = fbrq
                    spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                    conn.commit()
                except:
                    pass
        except:
            pass
        # break
#       下城区人社局       http://www.xcrcw.com/news_c1.html
def xcrs():
    qy = '下城区'
    ly = '人社局'
    url = 'http://www.xcrcw.com/news_c1.html'
    aaa = requests.get(url=url, headers=headers).text
    # print(aaa)
    aaa = re.findall('class="n-article-list"(.*?)<p>版权所有',aaa,re.S)[0]
    lists = re.findall('<a href="(.*?)" target="_blank">(.*?)</a></p><span>(.*?)</span></li>',aaa,re.S)
    # print(lists)
    for li in lists:

    #     if '.pdf' == li[0][-4:]:
    #         continue
    #     print(li)
        li = list(li)
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]

        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:

                nr = requests.get(url=wylj, headers=headers).text

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                # 'P>附件：<A href="http://www.xcrcw.com/index.php?m=index&amp;c=batch.download&amp;aid=801" target="_blank">'
                fjdzs = re.findall('href="(http://www\.xcrcw\.com/index\.php\?m=index&amp;c=batch\.download&amp;aid=.*?)" target="_blank">', nr)

                if fjdzs != []:
                    for i in fjdzs:
                        # if '@'  in i:
                        #     continue
                        # if 'http' not in i:
                        #     i = 'http://hrss.hangzhou.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                        # print(i)
                else:
                    fjdz = fjdz +'未解析出附件地址'
                print(fjdz)
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       下城区总     http://www.hzxc.gov.cn/col/col1489405/index.html
def xcrskj():
    qy = '下城区'
    url = 'http://www.hzxc.gov.cn/module/xxgk/xcmh_xxgkiframe1.jsp'

    aaa = requests.post(url=url, headers=headers).text
    # for i in aaa:
    lists =re.findall('<a href="(.*?)" title="(.*?)" target="_blank">.*?<span class="sub_tab_span1">.*?</span>.*?<span class="sub_tab_span2"><span style="display: inline;" syh=".*?" gkfs=".*?" jg="(.*?)".*?rq="(.*?)"',aaa,re.S)
    for li in lists:
        # print(li)
        wylj = li[0]
        bt = li[1]
        fbrq = li[3]
        ly = li[2]

        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://www.hzsc.gov.cn/art/2019/7/30/art_1267801_36196407.html', headers=headers).text.encode('latin-1').decode('utf8')
                nr = requests.get(url=wylj, headers=headers).text
                # print(nr)

                fjdz = ''
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                if fjdzs != []:
                    for i in fjdzs:
                        if '@'  in i:
                            continue
                        if 'http' not in i:
                            i = 'http://hrss.hangzhou.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                else:
                    fjdz = fjdz +'未解析出附件地址'
                print(fjdz)

                qy = qy
                ly = ly
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass
        # break
#       江干区总        http://www.jianggan.gov.cn/index.html
def jgrskj():
    qy = ' 江干区'
    url = 'http://www.jianggan.gov.cn/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    aaa = re.findall('html(.*?)news_clum_right',aaa,re.S)[0]
    lists = re.findall('title="(.*?)</a> </span><span style="float:right">.*?<a href="(.*?)" target="_blank">(.*?)</a></span></li>.*?</ul>',aaa,re.S)
    for li in lists:
        wylj = 'http://www.jianggan.gov.cn'+li[1]
        bt = li[0]
        fbrq = li[2]
        fbrq = str(fbrq).strip()


        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
               # nr = requests.get(url='http://www.jianggan.gov.cn/art/2019/12/5/art_1358710_40762754.html', headers=headers).text.encode('latin-1').decode('utf8')
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<a href="(/module/download/downfile\.jsp\?classid=0&filename=.*?)">', nr)
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@'  in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.jianggan.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                else:
                    fjdz = fjdz +'未解析出附件地址'
                print(fjdz)
                #
                qy = qy
                try:
                    ly = re.findall('<li style="float.*?;">来源：(.*?)</li>',nr,re.S)[0]
                except:
                    ly = ''
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                # cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                # conn.commit()
            except:
                pass

            # break

            # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       江干人社局        http://hrss.hangzhou.gov.cn/col/col1587845/index.html
def jgrs():
    qy = '江干区'
    url = 'http://www.jianggan.gov.cn/col/col1358710/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall(' <li><span style=".*?target="_blank">(.*?)</a></span> <span style="float:right"><a href="(.*?)" target="_blank">(.*?)</a></span></li> ]]></record>',aaa,re.S)
    # # print(lists)
    for li in lists:
    #     if '.pdf' == li[0][-4:]:
    #         continue
    #     print(li)
        li = list(li)
        if 'http' not in li[1]:
            'http://www.jianggan.gov.cn/art/2020/3/20/art_1358710_42342504.html'
            li[1]='http://www.jianggan.gov.cn'+li[1]
        wylj = li[1]
        bt = li[0]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)
        # print(fbrq)
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://www.jianggan.gov.cn/art/2019/12/5/art_1358710_40762754.html', headers=headers).text.encode('latin-1').decode('utf8')
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<a href="(/module/download/downfile\.jsp\?classid=0&filename=.*?)">', nr)
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@' in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.jianggan.gov.cn' + i
                        fjdz = fjdz + i + '\n'
                else:
                    fjdz = fjdz + '未解析出附件地址'
                print(fjdz)
                #
                qy = qy
                try:
                    ly = re.findall('<li style="float.*?;">来源：(.*?)</li>', nr, re.S)[0]
                except:
                    ly = ''
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                conn.commit()
            except:
                pass


        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       江干科技局        http://www.jianggan.gov.cn/col/col1257267/index.html
def jgkj():
    qy = '江干区'
    url = 'http://www.jianggan.gov.cn/module/xxgk/search.jsp?infotypeId=A01005&vc_title=&vc_number=&vc_filenumber=&area='
    # aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    data = {
        'infotypeId':'0',
        'jdid':'2143',
        'divid': 'div1256933',
        'infotypeId': 'A01005',
    }
    aaa = requests.post(url=url, headers=headers,data=data).text
    # print(aaa)
    lists = re.findall('''<a href='(.*?)' target='_blank' title='(.*?)' class='bt_link' style='line-height:35px;' >.*?</a></td><td align='center' width='80'>(.*?)</td><td align='center' width='180'>(.*?)</td>''',aaa,re.S)
    # print(lists)
    #                    '''<a href='' target='_blank' title='丁兰街道顺利举行江干区“巡河大PK，秀水大作战”系列活动暨 “世界水日大接龙”主题活动启动仪式' class='bt_link' style='line-height:35px;' >丁兰街道顺利举行江干区“巡河大PK，秀水大作...</a></td><td align='center' width='80'>2020-03-23</td><td align='center' width='180'>丁兰街道</td>'''
    for li in lists:

        wylj = li[0]
        bt = li[1]
        ly = li[3]
        # print(bt)
        # print(wylj)
        # print(fbrq)
        # print(ly)
    #

        try:
            # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
            # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
            # print(nr)
            nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
            # print(nr)
            # 'href="/attach/-1/2001091448071436013.docx"'
            # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
            fbrq = ''
            try:
                fbrq = str(re.findall('">发布时间：(.*?)</li>', nr, re.S)[0]).strip()
            except:
                pass

            if fbrq == rq_:
                print(bt)
                print(wylj)
                print(fbrq)

                fjdz = '未解析出附件地址'
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                # fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))" ', nr)
                # '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)
                #
                # if fjdzs != []:
                #     for i in fjdzs:
                #         if '@'  in i:
                #             continue
                #         if 'http' not in i:
                #             i = 'http://hrss.hangzhou.gov.cn' + i
                #         fjdz =fjdz +i+'\n'
                #         print(i)
                # else:
                #     fjdz = fjdz +'未解析出附件地址'
                print(fjdz)
            # #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
        except:
            pass



        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       拱墅区政府（包含人社局）        http://www.gongshu.gov.cn/col/col1496734/index.html
def gsrs():
    qy = '拱墅区'
    ly = '政府（包含人社局）'
    url = 'http://www.gongshu.gov.cn/col/col1496734/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall('<li><span class="date">(.*?)</span><a href="(.*?)" target="_blank">(.*?)</a>',aaa,re.S)
    # print(lists)
    for li in lists:
    #     if '.pdf' == li[0][-4:]:
    #         continue
    #     print(li)
        li = list(li)
        if 'http' not in li[1]:
            'http://www.gongshu.gov.cn/art/2020/3/2/art_1230043_42167309.html'
            li[1]='http://www.gongshu.gov.cn'+li[1]
        wylj = li[1]
        bt = li[2]
        fbrq = li[0]

        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                try:
                    fbrq = re.findall('<!--<\$\[信息显示时间\]>begin-->(.*?)<!--<\$\[信息显示时间\]>end-->', nr, re.S)[0]
                except:
                    pass
                # print(fbrq)
                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@'  in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.gongshu.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                        # print(i)
                else:
                    fjdz = fjdz +'未解析出附件地址'
                # print(fjdz)
                # print('===============')
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)

                # print(fjdz)

                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#        拱墅区科技局       http://www.gongshu.gov.cn/col/col1230548/index.html
def gskj():
    qy = ' 拱墅区'
    ly = '科技局'
    url = 'http://www.gongshu.gov.cn/col/col1230548/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall('<div class="list"><a href="(.*?)" target="_blank">(.*?)<span class="time">(.*?)</span></a></div>]]></record>',aaa,re.S)
    # # print(lists)
    for li in lists:
        # if '.pdf' == li[0][-4:]:
        #     continue
        # print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://www.gongshu.gov.cn/art/2019/10/8/art_1230548_38656696.html'
            li[0]='http://www.gongshu.gov.cn'+li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)
    #
    #
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                try:
                    fbrq = re.findall('<!--<\$\[信息显示时间\]>begin-->(.*?)<!--<\$\[信息显示时间\]>end-->', nr, re.S)[0]
                except:
                    pass
                print(fbrq)
                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))" targe', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@'  in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.gongshu.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                        # print(i)
                else:
                    fjdz = fjdz +'未解析出附件地址'
                print(fjdz)
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       西湖区人社局        http://www.hzxh.gov.cn/col/col1365369/index.html
def xhrs():
    qy = '西湖区'
    ly = '人社局'
    url = 'http://www.hzxh.gov.cn/col/col1365369/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall("<li><a style='font:9pt;line-height: 22px;'.*?href='(.*?)' class='bt_link' title='(.*?)'>.*?</a>.*?<span class='bt_time'>(.*?)</span><br></li>]]></record>",aaa,re.S)
    # print(lists)
    for li in lists:
    #     if '.pdf' == li[0][-4:]:
    #         continue
    #     print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://www.hzxh.gov.cn/art/2020/3/5/art_1365369_42100232.html'
            li[0]='http://www.hzxh.gov.cn'+li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)
    #
    #
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                nr = re.findall('html(.*?)<!--===================文章列表end=======================--></td>',nr,re.S)[0]

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))"', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@'  in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.hzxh.gov.cn' + i
                        fjdz =fjdz +i+'\n'
                        # print(i)
                else:
                    fjdz = fjdz +'未解析出附件地址'
                print(fjdz)
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       西湖区科技局        http://www.hzxh.gov.cn/col/col1177988/index.html
def xhkj():
    qy = '西湖区'
    ly = '科技局'
    url = 'http://www.hzxh.gov.cn/col/col1177988/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    # print(aaa)
    lists = re.findall("<li><a style='font:9pt;line-height: 22px;'.*?href='(.*?)' class='bt_link' title='(.*?)'>.*?</a>.*?<span class='bt_time'>(.*?)</span><br></li>]]></record>",aaa,re.S)
    # print(lists)
    for li in lists:
    #     if '.pdf' == li[0][-4:]:
    #         continue
    #     print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://www.hzxh.gov.cn/art/2020/3/5/art_1365369_42100232.html'
            li[0]='http://www.hzxh.gov.cn'+li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)
    #
    #
        if fbrq == rq_:
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                try:
                    ly = re.findall('<td>信息来源：(.*?)</td>',nr,re.S)[0]
                except:
                    pass
                print(ly)
                if '科技' in ly:


                    nr = re.findall('html(.*?)<!--===================文章列表end=======================--></td>',nr,re.S)[0]

                    fjdz = ''
                    # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                    fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))"', nr)
                    '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                    # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                    if fjdzs != []:
                        for i in fjdzs:
                            if '@'  in i:
                                continue
                            if 'http' not in i:
                                i = 'http://www.hzxh.gov.cn' + i
                            fjdz =fjdz +i+'\n'
                            # print(i)
                    else:
                        fjdz = fjdz +'未解析出附件地址'
                    # print(fjdz)
                    #
                    qy = qy
                    ly = ly
                    # xm = getxm(nr)
                    bt = bt
                    nr = nr
                    fjdz = fjdz
                    wylj = wylj
                    fbrq = fbrq
                    spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    # print(spider_time)
                    print(bt)
                    print(wylj)
                    print(fjdz)
                    print(ly)

                    cursor.execute(sql, (qy,ly,bt,nr,fjdz,wylj,fbrq,spider_time))
                    conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       滨江区人社局财政        http://www.hhtz.gov.cn/col/col1487002/index.html
def bjrs():
    qy = '滨江区'
    ly = '人社局'
    url = 'http://www.hhtz.gov.cn/col/col1487002/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    aaa = re.findall('<recordset>(.*?)</html>', aaa, re.S)[0]
    # print(aaa)
    lists = re.findall(
        '<a href="(.*?)" class="news" target="_blank">(.*?)</a>.*?<span class="time">\[(.*?)\]</span></li>]]></record>',
        aaa, re.S)
    # print(lists)
    for li in lists:
        #     if '.pdf' == li[0][-4:]:
        #         continue
        #     print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://www.hhtz.gov.cn/art/2020/3/23/art_1487002_42358499.html'
            li[0] = 'http://www.hhtz.gov.cn' + li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)
        #
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                try:
                    fbrq = \
                    re.findall('信息显示时间]>begin-->.*?<!--<\$\[信息显示时间\]>begin-->(.*?)<!--<\$\[信息显示时间\]>end-->', nr,
                               re.S)[0]
                except:
                    pass

                try:
                    ly = \
                    re.findall('信息来源]>begin-->.*?<!--<\$\[信息来源\]>begin-->(.*?)<!--<\$\[信息来源\]>end-->', nr, re.S)[0]
                except:
                    pass

                # print(fbrq)
                # print(ly)

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@' in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.hhtz.gov.cn' + i
                        fjdz = fjdz + i + '\n'
                        # print(i)
                else:
                    fjdz = fjdz + '未解析出附件地址'
                # print(fjdz)
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       滨江区科技局      http://www.hhtz.gov.cn/col/col1485817/index.html
def bjkj():
    qy = '滨江区'
    ly = '科技局'
    url = 'http://www.hhtz.gov.cn/col/col1485817/index.html'
    aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
    aaa = re.findall('<recordset>(.*?)</html>', aaa, re.S)[0]
    # print(aaa)
    lists = re.findall(
        '<a href="(.*?)" class="news" target="_blank">(.*?)</a>.*?<span class="time">\[(.*?)\]</span>.*?</li>]]></record>',
        aaa, re.S)
    # print(lists)
    for li in lists:
        #     if '.pdf' == li[0][-4:]:
        #         continue
        #     print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://www.hhtz.gov.cn/art/2020/3/23/art_1487002_42358499.html'
            li[0] = 'http://www.hhtz.gov.cn' + li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]
        # print(bt)
        # print(wylj)
        # print(fbrq)
        #
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                try:
                    fbrq = re.findall('<!--<\$\[信息显示时间\]>begin-->(.*?)<!--<\$\[信息显示时间\]>end-->', nr, re.S)[0]
                except:
                    pass

                try:
                    ly = re.findall('<!--<\$\[信息来源\]>begin-->(.*?)<!--<\$\[信息来源\]>end-->', nr, re.S)[0]
                except:
                    pass

                # print(fbrq)
                # print(ly)

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@' in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.hhtz.gov.cn' + i
                        fjdz = fjdz + i + '\n'
                        # print(i)
                else:
                    fjdz = fjdz + '未解析出附件地址'
                # print(fjdz)
                #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(spider_time)
                print(bt)
                print(wylj)
                print(fbrq)
                print(fjdz)

                cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       萧山人社局科技局        http://xxgk.xiaoshan.gov.cn/col/col1416436/index.html
def xsrskj():
    qy = '萧山区'
    ly = '政府'
    url = 'http://xxgk.xiaoshan.gov.cn/module/xxgk/search.jsp?area=&infotypeId=015&vc_title=&vc_number=&vc_filenumber='
    data = {
        'infotypeId': '0',
        'jdid': '2340',
        'divid': 'div1310567',
        'infotypeId': '015',
    }
    aaa = requests.post(url=url, headers=headers, data=data).text
    # print(aaa)
    lists = re.findall(
        '''<a syh=".*?" gkfs=".*?" jg="(.*?)" rq="(.*?)" mc="(.*?)" wh="".*?href='(.*?)' target='_blank' class='bt_link' style=".*?" >''',
        aaa, re.S)
    # print(lists)
    for li in lists:
        #     if '.pdf' == li[0][-4:]:
        #         continue
        #     print(li)
        li = list(li)

        wylj = li[3]
        bt = li[2]
        fbrq = li[1]
        ly = li[0]

        # print(bt)
        # print(ly)
        # print(wylj)
        # print(fbrq)
        #
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                try:
                    fbrq = re.findall('<span>发布日期：(.*?)</span>', nr, re.S)[0]
                except:
                    pass
                # print(fbrq)
                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@' in i:
                            continue
                        if 'http' not in i:
                            'http://xxgk.xiaoshan.gov.cn/art/2020/3/25/art_1416439_42384875.html'
                            i = 'http://xxgk.xiaoshan.gov.cn' + i
                        fjdz = fjdz + i + '\n'
                        # print(i)
                else:
                    fjdz = fjdz + '未解析出附件地址'
                # print(fjdz)
                # #
                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(spider_time)
                print(bt)
                print(wylj)
                print(fjdz)

                cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       余杭区人社局        http://www.yhqrcfw.com/Information/list.aspx?page=1&name=%D7%EE%D0%C2%D7%CA%D1%B6
def yhrs():
    qy = '余杭区'
    ly = '人社局'
    url = 'http://www.yhqrcfw.com/Information/list.aspx'
    aaa = requests.get(url=url, headers=headers).text
    # print(aaa)
    lists = re.findall(
        '</td><td height="26" class="border_b_x"><a class="" target="_blank" href="(.*?)">(.*?)</a></td><td style="" class="time">(.*?)</td></tr><tr>',
        aaa, re.S)
    # print(lists)
    for li in lists:
        if '.pdf' == li[0][-4:]:
            continue
        # print(li)
        li = list(li)
        if 'http' not in li[0]:
            'http://www.yhqrcfw.com/information/newsshow.aspx?artid=3387&classid=9'
            li[0] = 'http://www.yhqrcfw.com' + li[0]
        wylj = li[0]
        bt = li[1]
        fbrq = li[2]

        #
        if fbrq == rq_:
            print(bt)
            print(wylj)
            print(fbrq)
            try:
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                # print(nr)
                # nr = requests.get(url='http://www.yhqrcfw.com/information/newsshow.aspx?artid=3386&classid=137', headers=headers).text
                nr = requests.get(url=wylj, headers=headers).text
                # print(nr)
                # 'href="/attach/-1/2001091448071436013.docx"'
                # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'

                fjdz = ''
                # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))" target=_blank', nr)
                '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                if fjdzs != []:
                    for i in fjdzs:
                        if '@' in i:
                            continue
                        if 'http' not in i:
                            i = 'http://www.yhqrcfw.com' + i
                        fjdz = fjdz + i + '\n'
                        # print(i)
                else:
                    fjdz = fjdz + '未解析出附件地址'
                print(fjdz)

                qy = qy
                ly = ly
                # xm = getxm(nr)
                bt = bt
                nr = nr
                fjdz = fjdz
                wylj = wylj
                fbrq = fbrq
                spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print(spider_time)
                # print(bt)
                # print(wylj)
                # print(fjdz)

                cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                conn.commit()
            except:
                pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#     余杭区人社局科技局      http://www.yuhang.gov.cn/col/col1532245/index.html    http://www.yuhang.gov.cn/col/col1532238/index.html
def yhrskj():
    qy = '余杭区'
    ly = '政府'
    urls = ['http://www.yuhang.gov.cn/col/col1532238/index.html',
            'http://www.yuhang.gov.cn/col/col1532245/index.html']
    for url in urls:
        aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
        # print(aaa)
        lists = re.findall(
            '<li><a href="(.*?)" target="_blank"><span>(.*?)</span><i>(.*?)</i></a></li>]]></record>', aaa, re.S)
        # print(lists)
        for li in lists:
            if '.pdf' == li[0][-4:]:
                continue
            # print(li)
            li = list(li)
            if 'http' not in li[0]:
                'http://www.yuhang.gov.cn/art/2020/3/25/art_1532245_42388956.html'
                li[0] = 'http://www.yuhang.gov.cn' + li[0]
            wylj = li[0]
            bt = li[1]
            fbrq = li[2]
            # print(bt)
            # print(wylj)
            # print(fbrq)
            #
            #
            if fbrq == rq_:
                print(bt)
                print(wylj)
                print(fbrq)
                try:
                    # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                    # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                    # print(nr)
                    nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')
                    # print(nr)
                    # 'href="/attach/-1/2001091448071436013.docx"'
                    # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'
                    try:
                        fbrq = re.findall('<!--<\$\[信息显示时间]>begin-->(.*?)<!--<\$\[信息显示时间]>end', nr, re.S)[0]
                    except:
                        pass

                    try:
                        ly = re.findall('<!--<\$\[信息来源]>begin-->(.*?)<!--<\$\[信息来源]>end-->', nr, re.S)[0]
                    except:
                        pass
                    fjdz = ''
                    # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                    fjdzs = re.findall('">.*?<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))"><img', nr)
                    '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                    # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                    if fjdzs != []:
                        for i in fjdzs:
                            if '@' in i:
                                continue
                            if 'http' not in i:
                                i = 'http://www.yuhang.gov.cn' + i
                            fjdz = fjdz + i + '\n'
                            # print(i)
                    else:
                        fjdz = fjdz + '未解析出附件地址'
                    # print(fjdz)
                    #
                    qy = qy
                    ly = ly
                    # xm = getxm(nr)
                    bt = bt
                    nr = nr
                    fjdz = fjdz
                    wylj = wylj
                    fbrq = fbrq
                    spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    # print(spider_time)
                    # print(bt)
                    # print(wylj)
                    # print(fbrq)
                    print(fjdz)

                    cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                    conn.commit()
                except:
                    pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       钱塘新区杭州钱塘新区管理委员会        http://qt.hangzhou.gov.cn/col/col1657687/index.html  http://qt.hangzhou.gov.cn/col/col1657676/index.html
def qtxq():
    qy = '钱塘新区'
    ly = '杭州钱塘新区管理委员会'
    urls = ['http://qt.hangzhou.gov.cn/col/col1657676/index.html',
            'http://qt.hangzhou.gov.cn/col/col1657687/index.html']
    for url in urls:
        aaa = requests.get(url=url, headers=headers).text.encode('latin-1').decode('utf8')
        # print(aaa)
        lists = re.findall(
            "<li><span>(.*?)</span><a href='(.*?)' title='(.*?)' target='_blank'>.*?</a></li>]]></record>", aaa,
            re.S)
        # print(lists)
        for li in lists:

            # print(li)
            li = list(li)
            if 'http' not in li[1]:
                'http://qt.hangzhou.gov.cn/art/2020/3/25/art_1657687_42392609.html'
                li[1] = 'http://qt.hangzhou.gov.cn' + li[1]
            wylj = li[1]
            bt = li[2]
            fbrq = str(li[0]).replace('/', '-').strip()
            # print(bt)
            # print(wylj)
            # print(fbrq)
            #
            if fbrq == rq_:
                print(bt)
                print(wylj)
                print(fbrq)
                try:
                    # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                    # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                    # print(nr)
                    nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')

                    # 'href="/attach/-1/2001091448071436013.docx"'
                    # 'href="http://zjjcmspublic.oss-cn-hangzhou.aliyuncs.com/jcms_files/jcms1/web3163/site/attach/-1/1912200945013926562.xlsx"'

                    fjdz = ''
                    # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                    fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                    '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                    # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                    if fjdzs != []:
                        for i in fjdzs:
                            if '@' in i:
                                continue
                            if 'http' not in i:
                                i = 'http://qt.hangzhou.gov.cn' + i
                            fjdz = fjdz + i + '\n'
                            # print(i)
                    else:
                        fjdz = fjdz + '未解析出附件地址'
                    print(fjdz)

                    #
                    qy = qy
                    ly = ly
                    # xm = getxm(nr)
                    bt = bt
                    nr = nr
                    fjdz = fjdz
                    wylj = wylj
                    fbrq = fbrq
                    spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    # print(spider_time)
                    # print(bt)
                    # print(wylj)
                    # print(fjdz)

                    cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                    conn.commit()
                except:
                    pass

                # break

                # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
#       钱塘新区杭州钱塘新区管理委员会2       http://www.hangzhou.gov.cn/col/col1255929/index.html
def qtxq2():
    qy = '钱塘新区'
    ly = '钱塘新区管理委员会'
    url = 'http://www.hangzhou.gov.cn/module/xxgk/search.jsp?infotypeId=&vc_title=&vc_number=&vc_filenumber=&area='
    data = {
        'infotypeId': '0',
        'jdid': '149',
        'divid': 'div1269023',
    }
    aaa = requests.post(url=url, headers=headers, data=data).text
    # print(aaa)
    lists = re.findall(
        '''<a style=" padding-left:10px; background:url\(http:.*?\) left center no-repeat;line-height:33px; padding-left:8px; font-size:14px; font-family:'微软雅黑';" href='(.*?)' target='_blank' title='(.*?)' ><a syh=".*?" jg="(.*?)" rq="(.*?)" mc=".*?" wh="" onmouseover='showtips.*?</a></td>''',
        aaa, re.S)
    # print(lists)
    for li in lists:

        # print(li)

        wylj = li[0]
        bt = li[1]
        lyy = str(li[2]).strip()
        fbrq = li[3]
        # print(bt)
        # print(wylj)
        # # print(lyy)
        # print(fbrq)
        #
        # #
        if fbrq == rq_:
            if lyy == '钱塘新区':
                print(bt)
                print(wylj)
                print(fbrq)
                try:
                    # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/9/2/art_1587845_37430794.html', headers=headers).text.encode('latin-1').decode('utf8')
                    # nr = requests.get(url='http://hrss.hangzhou.gov.cn/art/2019/12/27/art_1587845_42195123.html', headers=headers).text.encode('latin-1').decode('utf8')
                    # print(nr)
                    nr = requests.get(url=wylj, headers=headers).text.encode('latin-1').decode('utf8')

                    fjdz = ''
                    # fjdzs = re.findall('<A href="(.*?).docx" ', nr)
                    fjdzs = re.findall('<[a,A] href="(.*?(?:docx|xlsx|files|xls|zip|pdf))">', nr)
                    '<A href="/attach/-1/2003091643145089050.docx" target=_self><U>'
                    # fjdzs = re.findall('<(?:A|a) href="(.*?(?:docx|xlsx|files|xls))" ', nr, re.S)

                    if fjdzs != []:
                        for i in fjdzs:
                            if '@' in i:
                                continue
                            if 'http' not in i:
                                i = 'http://www.hangzhou.gov.cn' + i
                            fjdz = fjdz + i + '\n'
                            # print(i)
                    else:
                        fjdz = fjdz + '未解析出附件地址'
                    print(fjdz)

                    qy = qy
                    ly = ly
                    # xm = getxm(nr)
                    bt = bt
                    nr = nr
                    fjdz = fjdz
                    wylj = wylj
                    fbrq = fbrq
                    spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    # print(spider_time)
                    # print(bt)
                    # print(wylj)
                    # print(fjdz)

                    cursor.execute(sql, (qy, ly, bt, nr, fjdz, wylj, fbrq, spider_time))
                    conn.commit()
                except:
                    pass

        # break

        # '字段包括：区域，来源，项目，标题，内容，附件地址，网页链接，发布日期，发布时间   spider调度时间 '
def cleansjk():
    conn = pymysql.connect(host='192.168.2.97', user='root', password='BOOT-xwork1024', database='spider',
                           port=3306)

    cursor = conn.cursor()
    cleansql = """DELETE FROM policy_spider
    WHERE  bt IN (SELECT t.bt                    FROM   (SELECT bt
                                FROM   policy_spider
                                GROUP  BY bt
                                HAVING Count(bt) > 1) t)
       AND id NOT IN (SELECT dt.id
                      FROM   (SELECT Min(id) AS id
                              FROM   policy_spider
                              GROUP  BY bt                          HAVING Count(bt) > 1) dt);"""
    cursor.execute(cleansql, )
    conn.commit()
    print('去重成功！')
def alltest():
    print('=======================================================================================================')
    print('=======================================================================================================')
    print('浙江省省科技厅'+'今日有以下数据更新：')
    skjt()
    exit()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('杭州人社局'+'今日有以下数据更新：')
    hzrs()
    exit()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('杭州科技局'+'今日有以下数据更新：')
    hzkj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('上城区'+'今日有以下数据更新：')
    scrskj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('下城区'+'今日有以下数据更新：')
    xcrs()
    xcrskj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('江干区'+'今日有以下数据更新：')
    jgrs()
    jgkj()
    jgrskj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('拱墅区'+'今日有以下数据更新：')
    gsrs()
    gskj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('西湖区'+'今日有以下数据更新：')
    xhrs()
    xhkj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('滨江区'+'今日有以下数据更新：')
    bjrs()
    bjkj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('萧山区'+'今日有以下数据更新：')
    xsrskj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('余杭区'+'今日有以下数据更新：')
    yhrs()
    yhrskj()

    print('=======================================================================================================')
    print('=======================================================================================================')
    print('钱塘新区'+'今日有以下数据更新：')
    qtxq()
    qtxq2()
    cleansjk()
    quit()

alltest()

