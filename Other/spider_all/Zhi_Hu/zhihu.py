import re
import time
import json
import pymysql
import requests
'''
字段：
    id、keyword、title、url、be_praised_count、be_commented_count、answers_count、be_attention_count、
    be_watched_count、content、topic_type
'''

def get_ip():
    dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
def request_data(url):
    headers = {
        'cookie': '_zap=322f132c-829c-4de3-bc53-518a034c450a; d_c0="AAAZJmDxbhGPTpCtW8Hag2g5VG6hlf_8-Q4=|1592283026"; _ga=GA1.2.800688044.1592283027; _xsrf=vu3ouddwSZrmDd3ipRyUJeb4gAi0e3WP; _gid=GA1.2.1682116480.1598231717; q_c1=2d73e23eea324db7af8431ac99a510a8|1598231748000|1598231748000; tst=r; l_n_c=1; o_act=login; r_cap_id="ODc1YzU1ZmQzNTA4NGE0MWEyODY0OGVlMDJlNzEwY2I=|1598256286|369b94994e28d4bd6921d14593700aaa74e47d2c"; cap_id="NjkwNzgwM2QwZTVlNGIwMmJiMjgyZGVhYjEyNDgwMjM=|1598256286|cb8e7081cc2593c248b6cf3e48e2c2fa19938d7d"; l_cap_id="YmM3ZjQ0NDZmMjZkNGZkNmFmOWQ5NzcyYzM5ZTMyYmQ=|1598256286|1c1cfc461dfb932dd78ef845f7ba3092235a22d2"; n_c=1; capsion_ticket="2|1:0|10:1598256464|14:capsion_ticket|44:MWU4NTgwMTRhNTVlNDk4Njg3OTVmMmIxNjI0ZDY0M2M=|90cee30c0a3dc6223cf20efab16ed6b3c26227e82ae7a58e01cc5d2b0c635692"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1598254495,1598256256,1598256327,1598256477; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1598256940; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1598257130|1598256965',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    response = requests.request(method='get', url=url, proxies=proxys[-1], timeout=10, headers=headers).content.decode('utf-8')
    return response
def parse_data(response,key):
    data = response.get('data')
    for i in data:
        try:
            title = i.get('highlight').get('title').replace('<em>','').replace('</em>','')
            # print(title)
            # continue
            be_praised_count = str(i.get('object').get('voteup_count'))
            be_commented_count = str(i.get('object').get('comment_count'))

            anwers_id = i.get('object').get('id')
            question_id = i.get('object').get('question').get('id')
            detail_url = 'https://www.zhihu.com/question/{}/answer/{}'.format(question_id,anwers_id)
            response = request_data(detail_url)
            answers_count1 = re.findall('查看全部(.*?)个回答', response, re.S)
            answers_count2 = re.findall('查看(.*?)个品牌推荐的回答', response, re.S)
            if len(answers_count1) != 0:
                answers_count = str(answers_count1[0])  # 回答
            elif len(answers_count2) !=0:
                answers_count = str(answers_count2[0])  # 回答
            else:
                answers_count = 'null'

            be_attention_count = str(re.findall('关注者.*?title="(.*?)"', response, re.S)[0])  # 关注
            be_watched_count = str(re.findall('被浏览.*?title="(.*?)"', response, re.S)[0])  # 浏览

            content = re.findall('ztext" itemProp="text">(.*?)</span>', response, re.S)
            if len(content) == 0:   # 正文
                content = 'null'
            else:
                content = str(content[0])

            topic_type = str(re.findall('<meta itemProp="keywords" content="(.*?)"', response, re.S)[0])  # 话题
            print({'key':key,'title':title,'detail_url':detail_url,'be_attention_count':be_attention_count,
                        'be_commented_count':be_commented_count,'be_praised_count':be_praised_count,
                        'be_watched_count':be_watched_count,'answers_count':answers_count,'content':content,
                        'topic_type':topic_type})
            sum.append({'key':key,'title':title,'detail_url':detail_url,'be_attention_count':be_attention_count,
                        'be_commented_count':be_commented_count,'be_praised_count':be_praised_count,
                        'be_watched_count':be_watched_count,'answers_count':answers_count,'content':content,
                        'topic_type':topic_type})
            # exit()
            time.sleep(2)
        except Exception as e:
            print('信息有误，直接跳过！！！')
            time.sleep(2)
            continue
def insert_db(data):
    '''
    id、keyword、title、url、be_praised_count、be_commented_count、answers_count、be_attention_count、
    be_watched_count、content、topic_type
    :param data:
    :return:
    '''
    global sum
    db = pymysql.connect(host='192.168.2.222', password='123456', database='test', user='root')
    cursor = db.cursor()
    for i in data:
        keyword = i.get('key').strip()
        title = i.get('title').strip()
        url = i.get('detail_url').strip()
        be_praised_count = i.get('be_praised_count').strip()
        be_commented_count = i.get('be_commented_count').strip()
        answers_count = i.get('answers_count').strip()
        be_attention_count = i.get('be_attention_count').strip()
        be_watched_count = i.get('be_watched_count').strip()
        content = i.get('content').strip()
        topic_type = i.get('topic_type').strip()

        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_created,gmt_updated = times,times

        sql = """insert into zhihu (id,keyword,title,url,be_attention_count,be_watched_count,answers_count,be_praised_count,
        be_commented_count,topic_type,content,gmt_created,gmt_updated)values(NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"""\
            .format(keyword,title,url,be_attention_count,be_watched_count,answers_count,be_praised_count,be_commented_count,topic_type,content,gmt_created,gmt_updated)
        cursor.execute(sql)
    db.commit()
    db.close()
    sum = []

def main():
    keywords =['创业','创业项目','商标注册','公司注销','公司注册','大学生创业','杭州创业政策','项目申报','代账','公司变更','高新认定','商标注册v版权认定','社保代缴']
    for key in keywords:
        url = "https://api.zhihu.com/search_v3?advert_count=0&correction=1&lc_idx=0&limit=20&offset=20&q={}".format(key)
        print(url)
        while 1:
            response = request_data(url)
            response = json.loads(response)
            choice = response.get('data')
            if choice == []:
                break
            else:
                parse_data(response,key)
                url = response.get('paging').get('next')
                print(url)

            time.sleep(2)
        insert_db(sum)

if __name__ == '__main__':
    sum = []
    proxys = []
    get_ip()
    main()