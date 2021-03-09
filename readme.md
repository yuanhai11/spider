### 爬虫项目整理：
```
 1、园区爬虫：
    请求方式：GET
    源url： https://www.qcc.com/more_zonesearch.html?p={}、https://s.tianyancha.com/parks/p{}
    表名：spider_park_data
    库名：99服务器下的 spider
    反爬措施：无
    更新策略：以园区id作为判断条件，布隆过滤器进行过滤出新的URL，并且入库，之后合并企查查和天眼查数据完成增量数据的增加
 2、园区-映射公司爬虫：
    请求方式：GET
    源url： 园区爬虫的url
    表名：spider_park_company_connect
    库名：99服务器下的 spider
    反爬措施：出现封账号，
    更新策略：无

  3、杰出人才爬虫：
    请求方式：POST
    源url：http://hrss.hangzhou.gov.cn/col/col1587845/index.html?uid=4840420&pageNum=2
    表名：spider_outstand_talent
    库名：99服务器下的spider
    反爬措施：数据POST请求的，参数要创建完整
    更新策略：本地爬过的url存在本地，下次爬取进行比对，得到更新数据，进行解析，存库

  4、公司荣誉名单爬虫：
    网页url：http://kjt.zj.gov.cn/art/2020/2/21/art_1228971341_41965076.html
            http://kj.hangzhou.gov.cn/art/2018/5/21/art_1693977_39157687.html
            http://www.hzsc.gov.cn/art/2019/7/30/art_1267801_36196407.html
            http://www.hzxc.gov.cn/art/2019/7/12/art_1509909_35884910.html
            http://www.jianggan.gov.cn/art/2018/11/22/art_1257287_25547419.html
            http://www.gongshu.gov.cn/art/2019/3/7/art_1240827_33920104.html
            http://www.hzxh.gov.cn/art/2019/1/21/art_1177988_29837555.html
            http://www.hhtz.gov.cn/art/2019/3/18/art_1485818_31303869.html
            http://www.xiaoshan.gov.cn/art/2020/3/5/art_1302903_42096721.html
            http://www.yuhang.gov.cn/art/2019/12/10/art_1601762_40955780.html
    表名：spider_company_honor_data
    库名：99服务器中的spider
    反爬措施：无
    更新策略：布隆过滤器进行过滤，将符合要求的详情页保存在spider_all_data表里，并根据url设置指纹信息，下次爬取时，信息的url加密与表里的进行比对，不存在-->入库，存在-->舍弃将详情页url存在本地库里，本地进行解析，最终入库到99服务器
    数据分布： 
        1、数据镶嵌在网页中；
        2、数据是docx/xlxs格式
```
Crawlab爬虫调度平台
- 硬件：
    linux系统，centos 7版本
- 软件：

    1、docker：19.03.13 安装参考：https://docs.docker.com/engine/install/centos/ 
    
    2、docker-compose：1.25.0 ，从github直接下载,并直接传到usr/local/bin下,名字改为docker-compose。
    
    3、touch docker-compose.yml，命令行工具，用来定义和运行容器，注意书写格式，用空格代表tab。

### Boss直聘
```
1/ 必须含有cookie里zp_token字段，cookie实效太短   方式：无界面浏览器，访问，保存cookie，request库进行爬取  （可行性不高）
```

### 企查查
```
目的：获取所有园区对应的公司名称。
注意：
    1、企查查会出现封账号的问题；
    2、爬取企查查公司数据不全；
    3、scrapy+本地脚本进行分块获取数据；
    4、定次更换ip+更换UA进行伪装；
结果：
    1、获取到园区对应的公司数据不全，企查查本身提供最多5000条公司数据；
    2、企查查官网里 7 个园区无公司数据；

反爬：
    封账号不封ip
    构建UA池、构建IP代理池
        无意发现的问题：关机重启后，再访问就不封账号了
```


