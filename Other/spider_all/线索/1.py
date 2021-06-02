import requests
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    # 'cookie':'Hm_lvt_c24dbbaefc81a78f7f07399d69a977df=1615943474,1615943485,1615943534,1615943590; Hm_lvt_f473aa29a53c9d4f36fff93ea9e202c6=1615943474,1615943485,1615943534,1615943590; Hm_lpvt_c24dbbaefc81a78f7f07399d69a977df=1615943644; Hm_lpvt_f473aa29a53c9d4f36fff93ea9e202c6=1615943644; dqmhIpCityInfos=%E6%B5%99%E6%B1%9F%E7%9C%81%E6%9D%AD%E5%B7%9E%E5%B8%82; JSESSIONID-PROD=23dc8484-0edb-4196-bb55-c145542d0fbd; svid=3AEC277C009DE3AED034FE5B0CA1F342; s_fid=07DD56FF92E85A65-00AF69368D8CF513; loginStatus=non-logined; lvid=97ab3970e35e7189b0692ecb844d558c; nvid=1; trkId=6B8FE877-F3D6-4FFF-833B-0959827BA4A6; s_cc=true; trkHmCitycode=0; lid=; COM.TYDIC.PAY.TRACE=2c0c8c73-32cd-4073-8d54-178f55991924; JSESSIONID_PERSONWEB=p389tgjGuZ65hHEt1Fi64nhXZ5O0qZo8F6IsbLY_W8IXgo9kzHoJ!872023340; Hm_lpvt_79fae2027f43ca31186e567c6c8fe33e=1615943092; Hm_lvt_79fae2027f43ca31186e567c6c8fe33e=1615943092; fenxiId=7a0a6677-ced9-4c9b-b537-6eda16ceb12c; cityCode=ah; SHOPID_COOKIEID=10013; trkintaid=jt-sy-yd-01; trkHmCoords=0; trkHmLinks=0; trkHmCity=0; trkHmPageName=0; trkHmClickCoords=0; s_sq=AZZA; JSESSIONID=l4Q5gRXRPGPkvF9yJhylFXThJL4HN2ByrM1rpyYmD8JQ15Qqp1BH!1620506823; Hm_lvt_333c7327dca1d300fd7235c159b7da04=1615943474; __session:0.5023005231550566:=http:; Hm_lpvt_333c7327dca1d300fd7235c159b7da04=1615943644'
}

res = requests.request('get',headers = headers,url='http://book.zongheng.com/rank/details.html?rt=4&d=1&i=0&c=1').text
from lxml import etree
data = etree.HTML(res)
url = data.xpath('//div[@class="rank_d_b_name"]/a/@href')
title = data.xpath('//div[@class="rank_d_b_name"]/a/text()')
print(url,title)


