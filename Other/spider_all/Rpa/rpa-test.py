import rpa as r

def main():
    r.init()
    # r.url('https://www.baidu.com')
    r.click(500,600)
    exit()

    print(r.text())
    print(r.read('//input[@id="su"]/@value'))
    r.close()
    r.type('//[@name="q"]', 'decentralization[enter]')
    print(r.read('result-stats'))
    r.snap('page', 'results.png')
    r.close()


def main2():
    r.init(visual_automation = True)
    r.click(100,100)
    exit()
    r.dclick('outlook_icon.png')
    r.click('new_mail.png')
    ...
    r.type('message_box.png', 'message')
    r.click('send_button.png')
    r.close()

def main3():
    r.init(visual_automation=True, chrome_browser=False)
    r.keyboard('[cmd][r]')
    r.keyboard('safari[enter]')
    r.keyboard('[cmd]t')
    r.keyboard('mortal kombat[enter]')
    r.wait(2.5)
    r.snap('page.png', 'results.png')
    r.close()

def main4():
    print(r.telegram('1234567890', 'ID can be string or number, r.init() is not required'))
if __name__ == '__main__':
    # main()
    # main2()
    # main3()
    main4()