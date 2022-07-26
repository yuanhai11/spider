import requests,time
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
}
init_url = "https://wuqi.supfree.net/ufo.asp?classify=warship&page="
detail_url = "https://wuqi.supfree.net/"
for page in range(1, 80):
    dd = requests.get(init_url + str(page),
                      headers=headers, timeout=10
                      ).content.decode("utf-8")
    # print(dd)
    tree_detail = etree.HTML(dd)
    lists = tree_detail.xpath('//div[@class="col-md-4"]/a/@href')
    for l in lists:
        json_data = {}
        url = detail_url + l
        content = requests.get(url,
                          headers=headers, timeout=10
                          ).content.decode("utf-8")
        # print(content)
        tree_detail = etree.HTML(content)
        json_data['name'] = "".join(tree_detail.xpath('//div[@class="entry"]/div[4]/h3/text()')).strip().replace("\t","").replace("\n","").replace("\r","")
        json_data['desc'] = "".join(tree_detail.xpath('//div[@class="entry"]/div[4]/p/text()')).strip()
        json_data['country'] = "".join(tree_detail.xpath('//div[@class="entry"]/div[4]/small/text()')).strip()
        json_data['import'] = "".join(tree_detail.xpath('//div[@class="entry"]/div[5]//text()')).strip()
        print(json_data)
        time.sleep(0.5)
