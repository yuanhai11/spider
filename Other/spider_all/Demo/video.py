# coding:utf-8
import requests
import time,re
from lxml import etree

# url_lists = ['http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=d311853f-c861-44d8-8a10-86c53b2d2a36&s=dc&t=VideoKnowledge&rn=015&h=menu&pi=1&mode=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=28fc3f28-e905-458d-baa9-723cb2ef0b4f&s=dc&t=VideoKnowledge&rn=017&h=menu&&ps=50&pi=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=c36da6df-2e0f-48b6-adf5-efe0733ee08a&s=dc&t=VideoKnowledge&rn=022&h=menu&pi=1&mode=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=4b6e0721-071d-4811-ac54-aeea17f1138e&s=dc&t=VideoKnowledge&rn=014&h=menu&pi=1&mode=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=c311e64f-f28b-490d-82ba-effeb472999d&s=dc&t=VideoKnowledge&rn=028&h=menu&pi=1&mode=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=aa69c2a3-2afb-4121-aca4-815f17346a00&s=dc&t=VideoKnowledge&rn=016.013.008.004&h=menu&pi=1&mode=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=d41da466-49a9-4699-9452-30188c33ceec&s=dc&t=VideoKnowledge&rn=016.017&h=menu&pi=1&mode=1',
#              'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=7b7560e9-455c-4b5d-a108-0a24ae12529d&s=dc&t=VideoKnowledge&rn=016.018&h=menu&pi=1&mode=1',
#              ]
#
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
#     'cookie':'route=c3bd1af43d8c66d907827d25287293a9; ELEARNING_00010=menu; ELEARNING_00025=|dc|2; ELEARNING_00008=3bc48ff6-fd21-4ffa-8f34-579dc6f65068; ELEARNING_00002=dongyanan; ELEARNING_00017=8e10398b-559a-4628-a6a4-0238d4d177c0; XXTOWN_COOKIE_00018=8af71de9-70f1-41ae-93ae-f449b2f33cad; ELEARNING_00999=1ta001shcifpknhzgn5smvhx; COOKIE_LANGAGES=zh; route=797bf68c9b8c7c6fd5358384c396cf6e; TY_SESSION_ID=72fbb19d-1511-400d-8dfd-8bc40c55d203; loginType=Pwd; ELEARNING_00003=StudyMenuGroup; .ASPXAUTH=2D5D620BD4FB2A6D7526AAE002107F9AECC301BCD044AC80A87FF0417C36E0C8B4C8601268A58618A8EAB405E961BD3A10F8B78F65050ACBDA63F83331FFFA547E55D2D92796F8C007C4AD4D5BEC8647F3823D7175460C95D34EDC8BCEDE1FA38877A9A502FCC6F1503BA02759DC3C5296222E49E6FB39CF36261BF4B92A5A5B994A33EBA4F6F5532B237E59; ELEARNING_00006=A28A637BBE442E697EFBF43C976F7AB02888DAE8C80A6DBC0DEA3BFC0037780376AF6D97E256912B20FDCFF149155F7188B093C5588EE70A1573A06FA019AAB7739EB4029CDB33CFF52EC9E435127862058FD3752B64D07522E9B4658BF6753F3B5006865CAD2B7FFC30536EB963C132038A0A1F5A7C666AB45E44CA74170039271F79D6C82B2241A7685BC31BF8A14AC7B75B26FF20620109D4C447FD3B1176401CC2436A09C6FF0E9050684C85A89904777C1D1DDB36C4A72834DF; ELEARNING_00018=kEWTaJi27uTd9D18eKs0pzbvrbT1S9g4Qu68ZG1s9/X7Dm6AQEIcttV1lGyFzygOIqHo+9XlYXa7NLIy9WAQwFGCsaBteO+XitIcGBJi/nimQQK7ks/vJ1mGr4e1qwaHZDRCYQSoBMyHDQGhZbOGwihWZQm5BhjP2ZkapCVmKMJy5W8fJgRmuwbflCZXRoHH4Px7S7IgdFN/4O8NIFZtgwYpoe7leSNeseMBs8yO450=; ELEARNING_00024=ucloud--cluster--AAAAABjR4VD19Fz7HXmtEhUX0krhTBxUG-Sx1IIc3C3o8ko2hZiUMBwdsjJkQ6-o0wdJklTZr9wKib9CQxYsXrgji6HET-Cr45NkHmARmn2v1c5k5yXOFkmKwR-3YfumIAJ0DP16z7lzsuNVp14PLQwuxLQ; ELEARNING_00026=1'}
#
# single = {}
# for page in range(1,6):
#     url = 'http://edu.huisuanzhang.com/kng/knowledgecatalogsearch.htm?id=6cdccb58-2088-4864-aefb-2282ba8fbfaa&s=dc&t=VideoKnowledge&rn=016.014&h=menu&&ps=50&pi={}'.format(page)
#     response = requests.request(method='get',url=url,headers = headers).text
#     print(response)
#     tree = etree.HTML(response)
#     element_list = tree.xpath('//ul[@class="el-kng-img-list clearfix"]/li')
#
#     for ele in element_list:
#         detail_url = str(ele.xpath('./div[1]/img/@onclick')).split('/')[-1][:-4]
#         title = str(ele.xpath('./div[2]/div[1]/span/text()')[0])
#         print(detail_url,title)
#         single[detail_url] = title
#     time.sleep(2)
# print(single)

'''
{'a0cb997fd8f84259bc9c954d8e777f75.html': '慧算账企业版侯进忠', '21560ab49ecd4a6ba7923b986f56f922.html': '日报，邮箱，OA，网络学院使用公瑾大学版...', '5611ae87f8ff4103a4687d94de5ed00e.html': '公瑾大学套餐报价名称解释·', '17be4cdb24c04994800c217701b6129f.html': '会计部业务流程（公瑾大学简版）视频课', '6308590b17a0452fb316ebb301705874.html': '服务优势-公瑾大学版视频课', 'c085b3e5bd8b4b7783deaf63c02adb0c.html': '慧节税产品培训', '40d362c9b0ae4345bfc6a08dc62ae6d7.html': '慧算账财税业务平台产品介绍2019', 'f55c799f04884e699e3e1f0731e7715d.html': '38、业务处理+企业微信', '2a0971461906418da8591743d12bc1b9.html': '23、快递管理', '7bd87431e844465bbc8c9d764770e11d.html': '【总账会计】发票勾选认证视频讲解', '6c4d2ec6b94042dfbca83baffc5c3983.html': '【外勤/总账助理】自助机打印银行对账单...', '679a8bfb938246c9a294331a7cc62330.html': '11-13、客户转化（财税顾问）—移交记账', '326ae420fb08420ca895a6c6a2557010.html': '3（2）、一般人转小规模', '9debd138556246dfb9b6a2f71ab9d0db.html': '3（1）、小升一说明', 'a9ff7bef2551429f8d9f3153195f94ab.html': '43（2）、国内旅客运输发票录入说明', 'e93808ee3f3e4da186b3a76af6564866.html': '37、服务档案', '16f3a8d17d4e4cd7bdb35da14e9a91e4.html': '【总账会计】新人上岗SAP操作讲解-20200528', '678ba54f5c294c058e6982ca2dcc3f6d.html': '【财税顾问】新人上岗SAP操作讲解-20200527', 'd54e2c62e6fc49e98a0711696151fe13.html': '50（1）、成本核算-启用（总账会计）', '2cc66c8255b24eebb1b79ed15872f75a.html': '59、期末凭证', '48c669ee89e248cc8fd91865a6ca69b6.html': '49、折旧摊销（总账会计）', '72197748cc53401eae33b219e33043e2.html': '48 、工资管理（总账会计）', '0e42d64795a84af7802739e9e51b3fca.html': '46、资金流水（总账会计）', '64ab142f19154e6097279d88675d6a62.html': '45、费用模板（总账会计）', '06b476c93c594cebaa926c653284a2ce.html': '南通汪兰兰-切户沟通', 'dcbfeb6dbcab431e992fa46b17a3dea4.html': '北京海淀-续约沟通-坚持不懈，灵活变通，...', 'bf6e54c15f4b448eaf785be177d3a113.html': '南通冯金云-首次沟通', 'ec9e824235a246c997b3a1788720a21d.html': '北京朝阳陈立冲-不续约客户挽回', '9aeb781331954cdba5f1aac49f4ea60d.html': '上海黄浦吕培齐-续约沟通-逼单', '3c095e9a392c4166b867789b3b419a58.html': '上海徐汇刘礼燕-续约沟通', '6ac008ca389b49199b5cd442b098b0b8.html': '上海普陀吴玉珍-日常沟通-优秀', '1c55533d9fbc4784a24705a410a4cb68.html': '上海普陀徐兰兰-转介绍、推荐税控托管服务', 'cdd55b0ddc0f40519b29ee454229d41b.html': '上海普陀李雪妮-推荐税控托管', 'bb97348a67d6484f806e38df98c2a3d8.html': '电子口岸（单一窗口）退税申报系统操作篇', 'c899b50c2b03497a8f2117b4c7aba4bc.html': '出口退税培训二视频（实务篇）下', 'c0a19daf5db9496289e8d5f394b6a9aa.html': '出口退税培训三（系统操作篇）', '1d82b7f808cb4408ab201b1ee54165ed.html': '出口退税培训二视频（实务篇）', 'e6f94cb652cb453eaf020f0349555357.html': '慧算账企业版APP简介', '7e2294d3dfb04139ad340010c26606f8.html': '慧算账crm平台操作指引（基于v4.6版）', '6cf821a84ee54506a97b689f3c461ad6.html': '慧算账SAP整体功能介绍（基于V4.7）', 'afd3023d66bd43cbbc71280034490c01.html': '[民办非企业单位]', 'eeb7dfc5de454763985104dbb739021f.html': '慧算账出口退税专题培训（一）', '1bf3cb119cd54ccc94c9d1c2bbdfb8ae.html': '公瑾慧用车2020', '9a33932c585f4743a681023770b67d9c.html': '慧节税视频课程2020', '1a87e4f9ed4949489d4dd73f19b98a2c.html': '慧工宝培训视频0703', '7898eab3e2cd4db39ebeab3ed2f85e25.html': '公瑾慧用车-产品介绍', 'ed51d9b334024643b6f1e691ec238a79.html': '慧工宝-1', '65f22a0ee5c8400cb17dcda82aa621df.html': '高新企业认证培训课程视频', '7ad915ae89f5417faf3a38c74b308981.html': '慧工宝操作手册解析', '9f79ec09149a4a6c8dd4fe2e3501b472.html': 'FAQ', 'ccdabc4da3e445ee8aab5acc327aba9c.html': '慧工宝产品介绍', '59fb7404685a4aaaa344bfa599091665.html': '慧商机产品介绍', '9188a5dfac2a4f8db6f4b422ff773934.html': '慧算账宣传片0619', '2537f8b4c24e4d71a198419e1d2b5369.html': '小慧叭叭-6月', '590c65f8c9434e08a9d8b5f899a48c4b.html': '艺人ID-王龙华', '574e27c4605145348cf4a37393a098ba.html': '艺人ID-刘端端', 'e3f24eeb90ef42ea9ef6428ff22702d7.html': '艺人ID-王小利', 'eff925a1670046f78aac68a8b832e32f.html': '慧算账亮相中关村创业大街', '788e05c4a9034568896ce9cd659571f0.html': '荔枝FM', '943f82f9ce0d4c8bb718957f0f8ceb5a.html': '马苏-ID', 'fb1bfac4a8374df08fa1cc44125c613c.html': '慧算账品牌宣传相关规范', 'c375b0586da24a25a5f4903ff664447b.html': '慧算账快闪视频', '539fb2e5c35b4943be1c9e79bca3da4f.html': 'CRM_系列课程_合同签约1', 'c59e5dcee119497db5daf37e2227c3f0.html': 'CRM_系列课程_线索管理篇', 'ae1f8521a64a4f0fb7722df53995c7d4.html': '南通TOP张姝销售经验分享', 'f8f2cc050931440db649f98cefbe48f3.html': 'CRM使用-过程管理', '9bd177a852a24485b9b6bd10dbfcd695.html': 'CRM库-意向客户管理', '3eea0bbfe42f47bc8aef4b10ff6e6f50.html': '促单池运用＆如何提单', '9fe2d913a59e4996b4029ecce519c857.html': '如何标记客户意向级别', '2a4ec3caf0654c19976c09887240395d.html': '添加客户＆填写跟进记录', '83ee5c947cf94c73b79d66ea58c590c8.html': 'count计数函数', '3d9b14f23275479dae6562a57d100a53.html': '功能模块介绍', '6aa5fdeb22c84f0790e0be35b97a5f15.html': 'SUM加和函数相关'}

{'a0cb997fd8f84259bc9c954d8e777f75.html': '慧算账企业版侯进忠'}
{'21560ab49ecd4a6ba7923b986f56f922.html': '日报，邮箱，OA，网络学院使用公瑾大学版...'}
{'5611ae87f8ff4103a4687d94de5ed00e.html': '公瑾大学套餐报价名称解释·'}
{'17be4cdb24c04994800c217701b6129f.html': '会计部业务流程（公瑾大学简版）视频课'}
{'6308590b17a0452fb316ebb301705874.html': '服务优势-公瑾大学版视频课'}
{'c085b3e5bd8b4b7783deaf63c02adb0c.html': '慧节税产品培训'}             未录
{'40d362c9b0ae4345bfc6a08dc62ae6d7.html': '慧算账财税业务平台产品介绍2019'}
{'f55c799f04884e699e3e1f0731e7715d.html': '38、业务处理+企业微信'}
{'2a0971461906418da8591743d12bc1b9.html': '23、快递管理'}
{'7bd87431e844465bbc8c9d764770e11d.html': '【总账会计】发票勾选认证视频讲解'}
{'6c4d2ec6b94042dfbca83baffc5c3983.html': '【外勤/总账助理】自助机打印银行对账单...'}
{'679a8bfb938246c9a294331a7cc62330.html': '11-13、客户转化（财税顾问）—移交记账'}
{'326ae420fb08420ca895a6c6a2557010.html': '3（2）、一般人转小规模'}
{'9debd138556246dfb9b6a2f71ab9d0db.html': '3（1）、小升一说明'}
{'a9ff7bef2551429f8d9f3153195f94ab.html': '43（2）、国内旅客运输发票录入说明'}
{'e93808ee3f3e4da186b3a76af6564866.html': '37、服务档案'}
{'16f3a8d17d4e4cd7bdb35da14e9a91e4.html': '【总账会计】新人上岗SAP操作讲解-20200528'}
{'678ba54f5c294c058e6982ca2dcc3f6d.html': '【财税顾问】新人上岗SAP操作讲解-20200527'}
{'d54e2c62e6fc49e98a0711696151fe13.html': '50（1）、成本核算-启用（总账会计）'}
{'2cc66c8255b24eebb1b79ed15872f75a.html': '59、期末凭证'}    --------------------------
{'48c669ee89e248cc8fd91865a6ca69b6.html': '49、折旧摊销（总账会计）'}
{'72197748cc53401eae33b219e33043e2.html': '48 、工资管理（总账会计）'}
{'0e42d64795a84af7802739e9e51b3fca.html': '46、资金流水（总账会计）'}
{'64ab142f19154e6097279d88675d6a62.html': '45、费用模板（总账会计）'}

{'06b476c93c594cebaa926c653284a2ce.html': '南通汪兰兰-切户沟通'}
{'dcbfeb6dbcab431e992fa46b17a3dea4.html': '北京海淀-续约沟通-坚持不懈，灵活变通，...'}
{'bf6e54c15f4b448eaf785be177d3a113.html': '南通冯金云-首次沟通'}
{'ec9e824235a246c997b3a1788720a21d.html': '北京朝阳陈立冲-不续约客户挽回'}
{'9aeb781331954cdba5f1aac49f4ea60d.html': '上海黄浦吕培齐-续约沟通-逼单'}
{'3c095e9a392c4166b867789b3b419a58.html': '上海徐汇刘礼燕-续约沟通'}
{'6ac008ca389b49199b5cd442b098b0b8.html': '上海普陀吴玉珍-日常沟通-优秀'}
{'1c55533d9fbc4784a24705a410a4cb68.html': '上海普陀徐兰兰-转介绍、推荐税控托管服务'}
{'cdd55b0ddc0f40519b29ee454229d41b.html': '上海普陀李雪妮-推荐税控托管'}

{'bb97348a67d6484f806e38df98c2a3d8.html': '电子口岸（单一窗口）退税申报系统操作篇'}
{'c899b50c2b03497a8f2117b4c7aba4bc.html': '出口退税培训二视频（实务篇）下'}
{'c0a19daf5db9496289e8d5f394b6a9aa.html': '出口退税培训三（系统操作篇）'}
{'1d82b7f808cb4408ab201b1ee54165ed.html': '出口退税培训二视频（实务篇）'}
{'e6f94cb652cb453eaf020f0349555357.html': '慧算账企业版APP简介'}
{'7e2294d3dfb04139ad340010c26606f8.html': '慧算账crm平台操作指引（基于v4.6版）'}
{'6cf821a84ee54506a97b689f3c461ad6.html': '慧算账SAP整体功能介绍（基于V4.7）'}
{'afd3023d66bd43cbbc71280034490c01.html': '[民办非企业单位]'}
{'eeb7dfc5de454763985104dbb739021f.html': '慧算账出口退税专题培训（一）'}
{'1bf3cb119cd54ccc94c9d1c2bbdfb8ae.html': '公瑾慧用车2020'}
{'9a33932c585f4743a681023770b67d9c.html': '慧节税视频课程2020'}
{'1a87e4f9ed4949489d4dd73f19b98a2c.html': '慧工宝培训视频0703'}
{'7898eab3e2cd4db39ebeab3ed2f85e25.html': '公瑾慧用车-产品介绍'}
{'ed51d9b334024643b6f1e691ec238a79.html': '慧工宝-1'}
{'65f22a0ee5c8400cb17dcda82aa621df.html': '高新企业认证培训课程视频'}
{'7ad915ae89f5417faf3a38c74b308981.html': '慧工宝操作手册解析'}
{'9f79ec09149a4a6c8dd4fe2e3501b472.html': 'FAQ'}
{'ccdabc4da3e445ee8aab5acc327aba9c.html': '慧工宝产品介绍'}
{'59fb7404685a4aaaa344bfa599091665.html': '慧商机产品介绍'}
宣传片不录
# {'9188a5dfac2a4f8db6f4b422ff773934.html': '慧算账宣传片0619'}
# {'2537f8b4c24e4d71a198419e1d2b5369.html': '小慧叭叭-6月'}
# {'590c65f8c9434e08a9d8b5f899a48c4b.html': '艺人ID-王龙华'}
# {'574e27c4605145348cf4a37393a098ba.html': '艺人ID-刘端端'}
# {'e3f24eeb90ef42ea9ef6428ff22702d7.html': '艺人ID-王小利'}
# {'eff925a1670046f78aac68a8b832e32f.html': '慧算账亮相中关村创业大街'}
# {'788e05c4a9034568896ce9cd659571f0.html': '荔枝FM'}
# {'943f82f9ce0d4c8bb718957f0f8ceb5a.html': '马苏-ID'}
# {'fb1bfac4a8374df08fa1cc44125c613c.html': '慧算账品牌宣传相关规范'}
# {'c375b0586da24a25a5f4903ff664447b.html': '慧算账快闪视频'}
{'539fb2e5c35b4943be1c9e79bca3da4f.html': 'CRM_系列课程_合同签约1'}
{'c59e5dcee119497db5daf37e2227c3f0.html': 'CRM_系列课程_线索管理篇'}
{'ae1f8521a64a4f0fb7722df53995c7d4.html': '南通TOP张姝销售经验分享'}
{'f8f2cc050931440db649f98cefbe48f3.html': 'CRM使用-过程管理'}
{'9bd177a852a24485b9b6bd10dbfcd695.html': 'CRM库-意向客户管理'}
{'3eea0bbfe42f47bc8aef4b10ff6e6f50.html': '促单池运用＆如何提单'}
{'9fe2d913a59e4996b4029ecce519c857.html': '如何标记客户意向级别'}
{'2a4ec3caf0654c19976c09887240395d.html': '添加客户＆填写跟进记录'}
{'83ee5c947cf94c73b79d66ea58c590c8.html': 'count计数函数'}
{'3d9b14f23275479dae6562a57d100a53.html': '功能模块介绍'}
{'6aa5fdeb22c84f0790e0be35b97a5f15.html': 'SUM加和函数相关'}

'''


'''
('a02d2c3b9e784ba3a71edecdc0a2f900.html', '二次跟进')
('6a1ecc76c5a1408389fbc745a9a9d819.html', '工商流程（华南大区）')
('0b9d1ed32af34e51aa557b79f52715a3.html', '基础财税知识（华南大区）')
('62de859541a1404f815107b4a9c910cf.html', '异议处理')
('9f05f3a547e5404b94ad08be4f9a9fe7.html', '客户意向度判定')
('692ef53cf6904a21ab02601dc831148e.html', '挖需求')
('08c5070a72444311b1d7f96054b8fd68.html', '微信营销')
('0e2e15257d1b43e3b56cef3c4b435f10.html', '010总分机构 视频授课')




('1f713f2e04c54d26b52fcd869ab840ad.html', '007民非企业 视频授课')
('9524f444bf294695b52bab70f3e862a7.html', '012外资企业 视频授课')
('4c10d496108e4bba9948152b5afde7d2.html', '002差额征收 授课视频')
('5f57c7b2a6584e0598d1abcc429c74c5.html', '004软件即征即退 视频授课')
('5eb18a1efe784b299ef7bbb056ed1d6e.html', '011农产品行业 视频授课')
('5d7571b5ec8c44f09d6a94cde7225683.html', '001高新企业 授课视频')
('5eefbba4b882484592520788e6b6aef1.html', '003出口退税 视频授课')
('92580d0088af4f91b1cf9d28971543ab.html', '008建安行业 视频授课')
('9280afb584d34e26a8f523327042a9e2.html', '005工业行业视频授课')
('3afbcae6d7f94363b5a7dca771ec6216.html', '006贸易行业视频授课')
('e098f42a1692447d88bfdc5cd62c5295.html', '009现代服务业 授课视频分享')

('4c6fd6dac73849d681a13de92106c10e.html', '向思云一通价格痛点重点去深挖，最后引导...')
('1c4d1d8bfe6947a299bb688aa50e6a06.html', '曾国强一通电话针对代账公司税务政策普及...')   ------------ 

('aaa0246ad0db4ce08a107a6b2b0d3ebd.html', '徐州姜莉二通电话回访朋友做账')
('96488b8f75c542efbf30c94b4be7caeb.html', '徐州姜莉二通电话绝处逢生')
('d1ec91dab43b45bbbadea132676cb436.html', '林梦思多角度服务优势打动客户')
('aba3f55f20a94b519d1d9a4dbd70a2b9.html', '从工商异常开场深挖需求-嘉兴蔡小芳')
('e7ecb73948bd4347a793dcbffe20e82f.html', '如何挖掘已有会计的客户-嘉兴白利青')
('abd7409f1e9e474b871a7b2e33fcdfa9.html', '徐州姜莉赞美客户优秀录音')
('45229fd518dd44b8acef2861d61d593c.html', '徐州褚文旗一通电话起死回生优秀录音')
('f8265905fb4d4a07b49d5839c5d7b1e7.html', '泉州林梦思服务优势打动客户')
('4d3f68bc9b4c4fd3a3dd38e80c19aaf1.html', '泉州江健闽深入挖需求服务打动客户20190513')
('47e9a3572870497694cf6b1761a2fd85.html', '天分吴雅楠合理利用服务优势逼单')
('5c32e231113748c8979d8fc776772ef3.html', '广分杨倩倩服务优势，客户沟通')
('366d4a4acee149fdb4ca1addeac648bc.html', '北分张洪源税筹转化')
('0562effa7dc34b81804f632a5b794bcf.html', '北分陈少强报税节点切入，客户跟进，服务...')
('8218e5601e164dd8a4a4ac49fafeb172.html', '天分方珍珍专业知识打动客户')
('9323befacfd54f41a3441105245a6302.html', '济南赵建欣二通强势切户开场，成功邀约')
('20bb3d3325e3425ba468466740106d46.html', '济南邵宗彦不断缔结，强势沟通(完整版)')
('8760778cf1ed4bd888da0a1192b76cf5.html', '杭分刘贤富：二通通过专业性引导客户合作...')
('ee3104f8aedc4aebb7f4136e2e26d3f4.html', '济分赵建欣一通服务介绍逼单最终成交')
('c79e5eaed5d0468896c4fd0b01792c7f.html', '上分吴玉峰一通电话通过新政吸引客户建立...')
('af446b6a873347a5b098cb1ce0b40a99.html', '杭分吕丹萍-一通通过最新政策成功吸引客户')
('fcb193bd07554bd58fa0015fa111e4e6.html', '北分奚鹏来--服务优势打动客户')
('2836df6b4c6544dc8705e90ce0cca20e.html', '张慧爽-较好的危机渗透和举例子技巧')
('8c0e0c4e78084c888e7152bd16aa6b4d.html', '天分方珍珍商标切入')
('c860ccf3368c456c8b4639cb2c6fe14b.html', '上分程闪闪面对客户异议不卑不亢，一一解...')
('297f0eebd8ca4feb87814b24d6d5e82b.html', '吕丹萍-一通通过服务成功吸引客户')
('4133f24240e94d7688d0f6be8fd32423.html', '天分方珍珍服务优势，邀约')
('495ab66b218249a28a4350e30ee640a4.html', '济南徐亚凡新政策开场吸引客户')
('1eca355bc0e84694856392a15edf2fae.html', '杭分吕丹萍-二通通过促销成功吸引客户')
('641fc99fa1324df090861faff7c28a5f.html', '广分简沙二通电话新政吸引客户')
('d4ccf63ed5564889b62cdc1184c44ef9.html', '北分奚鹏来：一通电话，六次邀约，终见面')
('732a612781d043b182a0c45a1965bf4d.html', '天分郝秀萍不断邀约录音细节')
('081abfd43d87425f9f82a688cacef514.html', '上分李顺低意向客户转化')
('03914ac2837845aabddd86cefecd7eb0.html', '杭分吕丹萍-一通通过抓到客户痛点成功邀...')
('c92af3602b9649ec833e09a987cebe47.html', '广分郑通鑫月底逼单，异议处理')
('2633f0e59cf4433993a933f76f021d43.html', '北分奚鹏来--语气坚定要性十足成功约见客户')
('8666326985024edab8d498116779e306.html', '重分王清清 低意向客户转化 灵活邀约决策人')
('5fafef12fd144887a058c7371e51181b.html', '天分付营营一通电话成功发掘客户需求邀约')
('c95307546b2f46638777317fdb1dacd2.html', '济南彭珍珍服务优势合理避税')
('01faf0a5b67f46a7ab6ce187e1630dfc.html', '杭分吕丹萍-二通解决客户异议成功邀约客户')
('346fa58e8933439c8da29a33269075dd.html', '北分张慧爽-坚持+专业征服客户距离+不放...')
('c4c5a43c3c904eab984a4ea52703cfe1.html', '重分王清清 遇坐班会计灵活处理')
('65909f102b5f416c8c1a96ccb31eeb71.html', '天分方珍珍积极邀约，痛点制造')
('1ed39a7e20de4562b20b0fbf0ba12a65.html', '上分李顺一通电话超强专业知识攻克客户防线')
('95576134f6e84e2b8ba50a210cb07735.html', '杭分吕丹萍-二通抓住痛点用优势吸引邀约...')
('1cd55adf7f8345c1ac5d9ba7a929cf79.html', '广分潘琼华一通电话邀约')
('b269424e10c04082ae16896fc9ce38c3.html', '北分张慧爽：二通电话疑难问题巧妙回答')
('2ae33645e4b34c259ef0d9d7a1601683.html', '天分徐影一通电话邀约签单')
('1edb75c704af4a23bcbaf5055be12862.html', '上分杨华容一通电话确定意向立马邀约促销...')
('b1751edf7c1f41bdba48ce23dd76de80.html', '广分符白玟低意向客户转化') -------------

('de57f02316514bdaa888bf5de205f319.html', '重分田锇 二通电话回访')
('83507020214d4d8fa88b6dfcb7cdae93.html', '天分郝秀萍一通电话')
('67e49870cb74438db7be7ede7517fa8b.html', '济分辛明服务优势')
('32e3069236ce4575b4c2c2cd70abe36a.html', '广分郑通鑫交接问题解答录音')
('2fc224fd4a8e44d3b8d9e3c8f386ebcc.html', '北分张洪源服务对比要转介绍')
('a7378d79cc784c20933055fd39447c72.html', '重分王清清 针对未到期客户 巧妙为后期和...')
('7fb15dfa500d4ae998b571986b6b0447.html', '天分任翠翠介绍产品，积极邀约')
('988c8f7ae9094b2bad5da7eb7d09d9c1.html', '天分方珍珍一通电话')
('73f5efb0591346ad94ace8db92912226.html', '广分徐家丽无安全感客户服务介绍')
('08873ae67be24dfb8fe9304e072388a1.html', '北分马亚如：一般纳税人二通回访，重温旧梦')
('bedce1cebd9248809b535ab4c60a961b.html', '重分田锇 竞对 客户在一方财务的应对策略')
('86ecb705b32243f88b8171e4a7505a6d.html', '上分王艳丽，深入服务介绍，结合案例下危机')
('181336b660c24b6bb266d57ebc6ec10f.html', '济分石淑君二通回访录音')
('ac3a301397c54d43ad1a119de2c4b563.html', '广分黄柳清同行对比录音')
('f39f1e80fcbc4617b02403f77cd2a777.html', '北分张洪源服务优势录音')
('201354e043fe4705a82967843101cc7b.html', '石家庄通关话术尤欢')
('0592dbfeb36b4a7181ca4899c19cf15b.html', '石家庄-销售李秋平-通关录音')
('2f6c8435bba74951b0e7bd255c20b084.html', '东莞付必成')
('1728d2fefd234c86856bca6ec76397ba.html', '烟台销售李紫嫣通关录音')
('30b27ab3c51e4eb189bfbb2d9a2ae860.html', '济南王会 (1)')
('54562d558885465ea27012c014da9080.html', '广分郑通鑫')
('a3957395d63b48209d0647237dda2a8a.html', '广分简沙')
('626f3a6c41ea4a0685e3934ea9b0f5c5.html', '济南苏琼峰录音')
('a3c848538cc648ba8466cfe3a1854a7c.html', '慧算账第一届话术pk大赛获奖录音')
('0ff7b53988b24b19a455f7d808aa5db8.html', '重分田锇合理利用促销')
('3896c39bc3ad404ab29d9b4327f67b7a.html', '广分郑桂花服务优势，促销')
('a5ad990108ca47c696a8ccb4b7fcdb4d.html', '天分张凤一通电话')
('bde02ba214ff499683b528011c763790.html', '上分朱荣盛，不断提问，深挖需求，对症下药')
('e6adbd4813ba4c85ae79e091e316ce2a.html', '北分贾东月-利用促销活动成功约见客户')
('adcd6e67b619470fae1aef2ac5fa172a.html', '重分辜夕敏二通回访')
('4ed01cae1eb44185a5c232b230f5b0ca.html', '天分方珍珍一通电话')
('5880951748674d1eb8fde78e144740da.html', '上分唐洪岩，不断邀约，循序渐进')
('a629b01ef643470dabc7cf0941a975b1.html', '广分朱玲玲客户回访')
('f57996e4a77b4b36a84ef07bf140b85b.html', '北分赵启程-回访式开场+深挖客户痛点成功...')
('19f7fc955ece4d379e4d273be6533afe.html', '重分苟廷英 一通电话 专职会计 异议处理')
('0bb4f9e0e7ff490baf895060d371c067.html', '天分张凤专业角度凸显服务优势')
('49aae76ef8294a419c598b0873608548.html', '上分刘佩，挖掘客户需求，稳抓客户痛点')
('27c921693b344a80bce0bbe7f8ba420e.html', '广分李成龙一通电话客户服务解答')
('bfc0811795f8481aa391b87184b6ecf8.html', '北分张洪源-强势约见客户')
('5c0d4ae57849472190615309ec093e09.html', '重分田锇。朋友在做，异议处理')
('617bdfa133e742e6b5f0635e89b268f0.html', '天分张晓新需求挖掘，切入')
('6f3a49e707a5417ca14de9959ccb9e8a.html', '上分程闪闪熟悉财税政策及流程，给专业建议')
('1e894287ad57487292ab1e0a8f0d6045.html', '广分莫海慧一通跟进+客户异议解答')
('1e9f97bf42b542e98a32273252f292c5.html', '北分王国鹏（客户从排斥到见面）')
('009c8731c6fe4bcab1878150e7993a1b.html', '重分辜夕敏 一通电话 朋友代账  异议处理')
('dddb9bd2e8ad4f2cbbfbfc28582ce5a0.html', '天分车凯异议处理')
('6ab8525f1877429d9898fe1b20a973bf.html', '上分蔡可磊 客户痛点挖掘 服务优势')
('2c50f14dbe3c4c56b5dbbb1c76c2f006.html', '广分李猛一通竞对分析+异议解决录音细节')
('ed8f0645e0e945bc9ae3a9475a73a85d.html', '北分贾东月产品介绍及挖需求')
('b1c39e4badb749ad8f46488d010593ea.html', '上分李顺知己知彼，一通邀约成功录音细节')
('02ebc1ef25e64bd19689aea7b7c5737c.html', '北分赵凤原-切户挖需求录音细节')
('b191d663812e4817a3123a48d7a347b1.html', '北分黄佳楠一通电话 异议处理')
('cc21a5b06fc5407ebd7a24a1a514ce05.html', '重分辜夕敏 用财税专业知识打动客户')
('7d13464926f94804b4fe188629b42522.html', '天分张晓新需求挖掘，成功邀约')
('8730c4773303461d8e8e4c31358b4940.html', '重分王清清 个体户 朋友代账')
('fe6b96ddcfb94942870bcbdcfe50e0a6.html', '天分吴雅楠个性开场白，APP服务优势')
('adb24b116beb4b60969545b4d11475c8.html', '上分朱荣盛抓住痛点，狠狠刺激')
('08367156575f44469b7635edde70b6e9.html', '广分王丽珊二次跟进+服务介绍')
('cd3248444b6e4559b16cb71750dc20ec.html', '北分赵培二通电话录音细节')
('aceec51af2124e59802f7d7c4e8feeb2.html', '重分 李倩 竞对 猪八戒的客户 专业异议处理')
('79b638a01b0d41098e0c02dc89ca8ac5.html', '天分车凯需求挖掘录音')
('9d2f74b2e6654b438ec7bf3c8b3d4cdd.html', '上分林伟超强优势对比，不断异议处理，成...')
('ec5ca427c4c84d699b7b7ad2a8446c34.html', '广分陈伟清一通录音竞对分析，异议解决')
('58a9e2cbb0094e5b829dd385ea4a06ff.html', '北分曳春慧二通回访邀约志成')
('4e67f7ed1c3b4592a43678a4c3deaff5.html', '重分苟廷英一通电话')
('c08348e0e1bd4cc7b8cc2071f76b4117.html', '天分徐斯琪竞对对比录')
('0a73a9f43b504e63bda3c690d492f826.html', '上分乔啓发强势切户')
('24ba10da5a114224807abde0a0e6df61.html', '广分董馨泽产品介绍')
('459b50faa3cc49c69d3e8f379b2f87d6.html', '北分张慧爽一通电话需求挖掘')
('6f214152a649423c9605c717c7076f8d.html', '重分辜夕敏 一通电话 朋友代账 异议处理')
('154cb30d9a724dc98e446f22749a40a8.html', '天分方珍珍一通电话')
('49c04f3cbc6e4a1abaeb96bc1cf6503b.html', '上分陈利燕超强优势突出异议处理')
('3ce8f53fc797467295089a97bf53c424.html', '广分莫海惠一通渲染APP服务')
('9f7b191e8d7546cb9839427d8aa0c47b.html', '北分曳春慧异议处理，邀约')
('2738278f68ec411ba6cd1ec57a49fc9a.html', '天分吴雅楠服务优秀，促销录音')
('518faafb0c6543a791190612281e84b1.html', '上分陈祥异议处理服务优势')
('bc5536b4e29d4a04bee7ef12e2af5352.html', '广分谭建优惠促单')
('0a5432f7174342579c5713847d416d77.html', '北分朱贺开场白，挖需求，促销网签录2')
('607059cfd2ae40cebfdfabb319d72feb.html', '北分朱贺开场白，挖需求，促销网签录1')
('c95b886e48074e5c898c17088c904555.html', '北分栾妹萱客户沟通，异议处理')
('79f856200e7a409c98bb7af6861c46b6.html', '广分简沙注册客户邀约')
('546dd353cda540879e9abd5927df5b4d.html', '天分方珍珍-促销')
('0deeb07a61bf4ef7901d06768154ae1c.html', '重分田锇  一通电话 合理避税 挖需求 618...')
('dbeb3a5e3af64e6fbc6c966a93dcb438.html', '重分田锇 二通回访 找准决策人 财税异议...')
('919cce1dc8194734b71ed3eef8e36c5b.html', '天分赵焕博-基础服务')
('a319901e994341eabf29f8755e4bad48.html', '天分方珍珍-催逼单')
('d3f4cc66f49c45f396c9ab70a6187a76.html', '广分王敏注册客户开发')
('396c646310754b9cbbbaab7693a75075.html', '北分王丹丹二通电话')
('c4b9a825a5a0403da78005fade25f5c5.html', '田锇一通电话介绍服务优势 邀约见')
('b1f422eea60548f2802d8e90369ba8f8.html', '天分徐斯琪一通电话')
('213fcf88ec9a450fa8e2b9756bf36e0d.html', '上分蔡可磊强势邀约')
('c8b6648495d842d5b1480e27936c70e3.html', '赖培森个性开场+竞对分析')
('8d6e08982ab6457abc61241a092c6a1b.html', '北分杨明税筹转化录音')
('ea1b2a769e814d679cf62f39a9457d87.html', '重分周杨玲详细介绍服务优势')
('562cbbdaec0d42328c114775bee888a0.html', '天津方珍珍-二通电话邀约签单')
('422c9e32bdc1486799abaf30f925d0a0.html', '天分杨海珍用专业赢取客户信任')
('201a41668de046208441a1ec2fbeeb23.html', '广分郑爱莲客户异议解答+服务对比')
('4691e746bbdc43728a0a6ee09890d943.html', '北分贾洪亮一通电话')
('7776ee3c877042f5893e60860edcfbc1.html', '重分辜夕敏一通电话 成功获得转介绍')
('2e4fa6b52a694d71b1833a9746119981.html', '天分杨海珍一通电话')
('15c13e6ef62344628dd544829a9670ed.html', '深分郝运二通电话')
('7206bfae33514b8b9dbd92ca4c8694d7.html', '广分赖培森新客户开发+竞对分析')
('e213cc022ff349999051540f8497389b.html', '北分钟帆切户成交客户')
('0f357beafa874be5b75f0846b19cd4f3.html', '重分辜夕敏 二通电话回访 深度挖掘客户需求')
('2f3e4d1de41b48ef9980f1f425c2955b.html', '天分方珍珍二次跟进录音细节')
('24734fbf98a1427997477697ed93112b.html', '深分廖永凤逼单成交录音')
('2baa443b2cf64949991fc831cfa6740e.html', '广分唐海周客户回访，二次跟进')
('e0fa2954c3824fd8b2e62d8aa9c02e0c.html', '北分张洪源二通电话客户跟进')
('d88dfde6b0ec4863aa7f85a818c61967.html', '重分 苟廷英公司优势介绍')
('c9d44392fad84fd7bcfc527e252b146f.html', '天分张晋华天分张晋华服务优势')
('b223f315a72643d28a3e888cf840d4c6.html', '深分-李飞需求挖掘')
('637dd919586c436eb644a844a362419c.html', '广分吴娟客户开发')
('f064d431bfaa4f949aee12b85a15b97a.html', '北分张慧爽客户跟进')
('cfd7321e44714e5c9779374cc6a256c4.html', '天分吴雅楠一通电话')
('c0ad6fe482b2489c87d73538ceb925e9.html', '天分李立争一通电话')
('32c34a6215e04dfabc9ca90a3cc05006.html', '深分赖志鹏痛点挖掘')
('9898b35cc08246149cec5e11501b13cd.html', '广分冯伟杏新客户服务介绍+案例解答')
('204af61d1d514b24903ebb427801b8cc.html', '北分赵丹需求挖掘，服务优势')
('42a7c77e7c7a4cb88477892d0f2ef10f.html', '北分王冰客户跟进')
('a0f3ae5dcbb54b8496ea1dfaccfb30b9.html', '北分孙朝阳一通电话')
('d2b8318bcc6c4af7ad9d1c5ca1684618.html', '北分孙朝阳一通电话个性开场')
('99a56f9ee8614502b9bc37a10221385b.html', '北分李思思一通电话，服务优势')
('dbe4d126698f4eb386303d51f43cd738.html', '北分王国鹏切户成交')
('6296d9228dba4512bee247de3205482b.html', '北分王冰开场，服务优势')
('5be61609fdd947159391b1a2fc089827.html', '深分张志伟个性开场')
('d180dfec9e5a4392974bb89018ef5b19.html', '天分郝秀萍服务优秀，异议处理')
('b00fe17f93f34cff89daa4cb6fe196df.html', '天分杜佳荣服务优势，报价，邀约')
('b884d6dcf7954cd0a2d1c5f79cc2f485.html', '深分张志刚需求挖掘')
('5c394ad67d6f48039e64ae576cad66fd.html', '陈晓伟税筹产品转化录音1')
('442c8f875416450ca51bf70209b2ec46.html', '陈晓伟税筹产品转化录音2')
('68db8a95f9a542ff90a43a5295aaa36d.html', '天分马鸿薇促销逼单')
('31a4072f809e4b78b5ef20e96eb3ff67.html', '北分胡泽顺三类客户开发')
('9e3c8dc375014d5480aa058bcb78f1fe.html', '天分吴亚楠（异议处理）')
    ('4a075d0c2b394063a4fc82426cef2279.html', '上分谢珊，二通')
('613a1f3d1c2c4c24bf8ac13439c50389.html', '胡泽顺一通电话开三意向')

'''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'cookie':'route=c3bd1af43d8c66d907827d25287293a9; ELEARNING_00010=menu; ELEARNING_00025=|dc|2; ELEARNING_00008=3bc48ff6-fd21-4ffa-8f34-579dc6f65068; ELEARNING_00002=dongyanan; ELEARNING_00017=8e10398b-559a-4628-a6a4-0238d4d177c0; XXTOWN_COOKIE_00018=8af71de9-70f1-41ae-93ae-f449b2f33cad; ELEARNING_00999=xq1qrwoz413mff5vjdizdxhb; COOKIE_LANGAGES=zh; route=3bb5a1c73d06e1480174253c4bac43e2; TY_SESSION_ID=fc65cf50-f642-42a2-bf60-fd869c6414d3; loginType=Pwd; ELEARNING_00003=StudyMenuGroup; ELEARNING_00006=947B65575F16751EDD03F04CA5036DA968137AC0254E64576AF89077B04B9A64BB0934F25B78C2527141650434BDAC02D8F0D4D6B4EFAF789020CE621DAC0082C1CE0B955B2CADAFE26EB33248BAF1E4C7748703B86EF2200C216C4F45B6C4ED943D5AB954F906B7C284A554FB4A8DA692F5FE16E4CF2C3310B21317BF866F7F29A3F794765AD82FF98137511EFCBFCA0023C0B928539CDB55A542BD8CB6A848986C304DC3F7B7BA63E2B2C583F1A8F96EB058228CA28431D670D9BE; ELEARNING_00018=kEWTaJi27uTd9D18eKs0pysM6aroBGlolI9264tJl1mVCle78xBw5juveQbkKbCXLC+DSaF46jcCcSzm7JOwOITcc05lVBMrW/0IhdVAHO909rXQe69kvHpWZqCEZ8UyIfQoP/pw1ItuJbJmZw+g8cPdKvD9H7K7O0l3EzAbuewAg3BrdDnWcEB1hwQlAa3d2RY60wejnjv/JUwVcYRsDeC825TW3hK97llMGwhDefM=; ELEARNING_00024=ucloud--cluster--AAAAAHEk97RC5loOkNxt8BeJ0FZnzplzUP6SeaBd31d8IXpLkjZ3OGG9raoDCH4SBBJd_wB3u8QhmY_uSdZSF8Ro3mklVQiIZQOLOau5ff3aLILcrmDCboIfJ_3YJFahrJohu-wjHmusP_pDBMmMlvxp4iE; ELEARNING_00026=1; .ASPXAUTH=724258F7C162B8BBBA87327234A2DC67C52CBC904473DA31BA728702A17E2210DC48F7C59D88ECE39D15EF77779620D0B77E15837EA3FCE4C4473B2E3B39D45F821F70DC2033C34E6A7400A1D680D111D74AFD3AEAAE9AFBC2ABF789EE34D82DEBC36EBD89844001827C95F9E48FE25955A450B914E802189EED9183C86C20CCC57736A80C5FDB099A8FA87A'
}
data =['06b476c93c594cebaa926c653284a2ce.html','dcbfeb6dbcab431e992fa46b17a3dea4.html','bf6e54c15f4b448eaf785be177d3a113.html','ec9e824235a246c997b3a1788720a21d.html','9aeb781331954cdba5f1aac49f4ea60d.html','3c095e9a392c4166b867789b3b419a58.html','6ac008ca389b49199b5cd442b098b0b8.html','1c55533d9fbc4784a24705a410a4cb68.html','cdd55b0ddc0f40519b29ee454229d41b.html']
for i in data:
    url = 'http://edu.huisuanzhang.com/kng/view/video/'+ i
    response = requests.request(url=url,method='get',headers=headers).content.decode('utf-8')
    mp3 = re.findall(r'"audioFullPath":"(.*?)","imageFullPath"',response,re.S)
    print(mp3)

    tree = etree.HTML(response)
    title = tree.xpath('//span[@id="lblTitle"]/text()')[0]
    if len(mp3) !=0:
        mp3 = mp3[0]
    else:
        print('没有mp3')
        continue
    time.sleep(3)
    res = requests.request(url=mp3,method='get',headers=headers).content
    with open('{}.mp3'.format(title),'wb')as fp:
        fp.write(res)
    time.sleep(1)


