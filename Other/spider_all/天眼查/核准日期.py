import requests, re, pytesseract
from lxml.html import etree
from PIL import Image, ImageFont, ImageDraw, ImageColor

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # 若tesseract.exe安装在其他路径下，更改此处的指向路径

keyword = '京东'
headers = {
    'Cookie':'TYCID=e1e6efb0a5fc11e8af04cdd896ab5e5e; undefined=e1e6efb0a5fc11e8af04cdd896ab5e5e; ssuid=2739512828; _ga=GA1.2.1428665082.1536072517; RTYCID=1af95e55a4b54a88b4a9e12b0b316891; CT_TYCID=1e54f2e7bb7745f29ad8e0ef03c6de89; aliyungf_tc=AQAAABsd5kD4dgQAaMuedVOeS5fIGX2P; csrfToken=-l3eED3CM_gh3kqdYWzTNOCP; jsid=SEM-BAIDU-CG-SY-000700; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzYwNzY2OTQwNyIsImlhdCI6MTUzOTA0NzY4OSwiZXhwIjoxNTU0NTk5Njg5fQ.xnOALGRt-xDfQwjKK2ha-srf9acGAKX2knmeaxJeLhk6ejWn-5uRF2iVRowGFnUwEUFtYSArvJwGnlxUnwDMdA%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25221%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213607669407%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzYwNzY2OTQwNyIsImlhdCI6MTUzOTA0NzY4OSwiZXhwIjoxNTU0NTk5Njg5fQ.xnOALGRt-xDfQwjKK2ha-srf9acGAKX2knmeaxJeLhk6ejWn-5uRF2iVRowGFnUwEUFtYSArvJwGnlxUnwDMdA; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1539004455,1539047679,1539055612,1539070815; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1539070858; cloud_token=485d7821a19942fd9263c43cd7583486; bannerFlag=true',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Host': 'www.tianyancha.com'
}
Map_Dict = {}


def parse_detail_page(detail_page_source):
    '''
    解析详情页，提取字体文件中的id(/2d/2df8ui)，并提取公司的核准日期。
    问题一：如何解决已经解析过的字体文件不用重复解析？如果是解析过的，直接使用映射字典，不用再进行图片识别了。如果是没有解析过的字体文件，再进行图片识别。
    方案：声明一个字典，将解析过的字体id都存入列表中，等到后续获取字体id的时候，和字典中的id进行比对，查询是否存在这个id，如果已经存在，直接将映射字典取出。
    {'2df8ui':{'1':'2'},'b64s4f':{'1':'3'}}
    每一个id对应的映射字典是否保留？还是说只保留最新的id映射规则？
    都保留，避免刷新到以前的id时再重新解析一遍。
    :param data_tuple:get_detail_page()这个函数返回的元组。
    :return:
    '''
    obj = etree.HTML(detail_page_source, parser=etree.HTMLParser(encoding='utf8'))
    # 在详情页中提取字体id
    pattern = re.compile(
        r'<head>.*?<base.*?<link.*?href="https://static\.tianyancha\.com/fonts-styles/css/(.*?)/font\.css">', re.S)
    font_id = re.search(pattern, detail_page_source).group(1)
    # 在获取font_id以后，先判断Map_Dict中是否存在这个键，不存在再去调用parse_map_rule()
    if font_id not in Map_Dict:
        map_dic = parse_map_rule(font_id)
    else:
        map_dic = Map_Dict[font_id]
    print(map_dic)
    exit()
    # 根据映射  字典转换核准日期
    try:
        hezhunriqi = obj.xpath('//td[@colspan="2"]/text[contains(@class,"tyc-num")]/text()')[0]
        name = obj.xpath('//h1[@class="name"]/text()')[0]
        result = ''
        for char in hezhunriqi:
            if char != '-':
                real_num = map_dic[char]
                result += real_num
            else:
                result += '-'
        print(name, result)
    except:
        pass


def parse_map_rule(font_id):
    '''
    根据字体id，拼接woff字体文件，并对字体进行识别，最终将字体id和映射字典保存到一个全局字典中。
    :param font_id:
    :return:
    '''
    font_url = 'https://static.tianyancha.com/fonts-styles/fonts/{}/tyc-num.woff'.format(font_id)
    content = requests.get(font_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}).content
    with open('tyc.woff', 'wb')as f:
        f.write(content)
        # 先定义位置数字
        position_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        map_dict = {}
        for p_num in position_number:
            # 创建一个图片对象，用于后续数字图片的存储
            # (255,255,100) :RGB red/green/blue  三原色，每一种颜色的取值范围都是(0,255)
            # 三个参数：图片模式  图片的尺寸，图片的背景颜色
            img = Image.new('RGB', (300, 500), (255, 255, 100))
            draw = ImageDraw.Draw(img)
            # 根据位置数字p_num和字体文件woff，找出p_num在woff文件中的真实映射关系
            # 参数1：指定字体文件
            # 参数2：指定数字在画布上展示的大小
            # truetype()返回一个字体对象
            font = ImageFont.truetype('tyc.woff', 400)
            draw.text((10, 10), text=p_num, font=font, fill=ImageColor.getcolor('green', 'RGB'))
            img.save('tyc.png')
            # 利用pytesseract包识别图片中的数字
            # pip install pytesseract

            font_image = Image.open('tyc.png')
            num = pytesseract.image_to_string(font_image, config='--psm 6')
            if num == 'A' or num == '/':
                num = pytesseract.image_to_string(font_image, config='--psm 8')
                map_dict[p_num] = num
            elif num == '':
                map_dict[p_num] = p_num
            else:
                map_dict[p_num] = num
            # 有的字体文件中是缺少部分数字的，那么得到的图片就是一个空白的图片，也就是位置数字对应的真实数字不存在、
        # 凡是真实数字不存在的，都有一个特征：就是位置数字和真实数字是相等的。
        Map_Dict[font_id] = map_dict
        return map_dict


if __name__ == '__main__':
    url = 'https://www.tianyancha.com/company/2990217764'
    url = 'https://www.tianyancha.com/company/3168037664'
    res = requests.request(method='get',url=url,headers=headers).text
    parse_detail_page(res)
# 8627-93-97   1985-02-05
# 3986 - 83 - 88