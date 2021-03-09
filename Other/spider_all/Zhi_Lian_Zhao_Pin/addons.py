import mitmproxy.http
from mitmproxy import ctx

url_paths = 'https://fe-api.zhaopin.com/c/i/sou?_v'


class Jobinfo:
    def response(self, flow: mitmproxy.http.HTTPFlow):

        print('接受到了response！！！')
        if flow.request.url.startswith(url_paths):
            print('符合要求！！！')
            text = flow.response.content.decode('utf-8')
            with open('zhaopin.txt','a',encoding='utf-8')as fp:
                fp.write(text)

addons = [
    Jobinfo()
]