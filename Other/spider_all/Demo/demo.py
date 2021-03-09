import re
import requests
import os,time
file = os.environ.get('USERPROFILE')
topic_direct = os.path.join(file,'Desktop','GIF')
if not os.path.exists(topic_direct):
    os.mkdir(topic_direct)

def get_page(page_lists):
    for page in page_lists:
        url = 'http://www.hao123.com/gaoxiao/?pn={}'.format(page)
        return url

page_lists = [i for i in range(1,51)]
url = get_page(page_lists)
num = 0
for loop in page_lists:
    print(loop)
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }
    response = requests.get(url,headers = headers).content.decode('utf-8')
    source_url_lists = re.findall(r'<img selector="pic" img-src="(.*?)"',response,re.S)
    for index,source_url in enumerate(source_url_lists):

        topic_gif = requests.get(source_url,headers=headers).content
        name = source_url.split('/')[-1]
        with open('{}\\{}.gif'.format(topic_direct,num),'wb')as fp:
            fp.write(topic_gif)
            print('{}.gif load success'.format(num))
            num+=1

