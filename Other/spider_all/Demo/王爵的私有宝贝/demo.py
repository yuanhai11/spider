import requests
import random
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'cookie':'Hm_lvt_8366ffe221fee533dcf585e278cdcddc=1614736950; 1526_2566_125.120.149.239=1; 1527_2559_125.120.149.239=1; 2690_2327_125.120.149.239=1; 2689_2327_125.120.149.239=1; 1526_2525_125.120.149.239=1; 2690_2326_125.120.149.239=1; 2689_2326_125.120.149.239=1; 1526_2549_125.120.149.239=1; 1526_2554_125.120.149.239=1; 1526_2460_125.120.149.239=1; 1526_2444_125.120.149.239=1; 1526_2545_125.120.149.239=1; 1526_2325_125.120.149.239=1; 1526_2560_125.120.149.239=1; 1526_2563_125.120.149.239=1; 1526_2551_125.120.149.239=1; 1526_2454_125.120.149.239=1; 1526_2402_125.120.149.239=1; 1526_2511_125.120.149.239=1; Hm_lpvt_8366ffe221fee533dcf585e278cdcddc=1614739472; scoldviews_1527=jI6wkQy3mUyGTbRW0rZE0NkJnlhYoC%252Fe6Le0tUEk8G9EGQfEd%252FLLJjml7e243k5sF2TNUns4RvvCMZ1MSi5XVukzoQJUX5TgU0yxsRH5AWaSRZ%252BdAae5jzxLcpt1QyHeXlWih3Kr9JUeucyfQjp7Mc8t23Z%252B27%252BUDItNXly4h5dB9ZVYmBDY2x5rGVY%252FVJDTX47I4YyZQfP43My7inJp9U08u9BfGGbrDuc7YIbTDIQyiTgrbViCdpY65yqX0Bm3nL%252FbG2aQyRrHuCWq0fwNDQdd3cfpiVAFVarGtSyQNzTP8wtk7mpiO%252B2f%252BYFEdy0LmZOa8Bm9do6S%252BiyaK7809A%253D%253D; 1527_2455_125.120.149.239=1; richviews_1526=jIwXE7vEJli4JVOueftGea6XpVwMSR3MlFPmREjfTMZgP%252BJwvq%252B1MW0fCYrDyQhXnSB%252Bvl09UJBtGegZEDXHXXT6uDFF0p0Gw%252FLagTpME9xH1Ue9ziBWFnXoCA7dRoeaYYudLF0a09LT0XjO5%252F1MV9OtDpCY%252BXkPvoGNPidvFq30N7EErFcrLiBQYaKTuCalVU2FDncpvbKBbATzNA92L12gQc8NpcHIz5iltT3JojUtggig558Z9O290fXFBmpWdNCpSUaT9Nrr3PieDfnRx33WR%252BgyzjOcZhORaHX8jkgm6RLxi2LTzI5heMSJVBqtI2yoXAvg69lmw3XYlPXP3luoAqnGqMHEWI9bzY%252Fy4e3h4IY0QMxAh%252FW5fu7qEk2vTUAR3JK9JRQqW9MZOEC%252FCN72mfKEiV8JIKIRxRii8DZnHbZehQlymNr2J0EgISnJWHZOJMsK5WW7oshOtdM5Iu4%252FUy4%252BQT2ElIH6xN3tdtgO1obInCXX2G41yueQYN5lLivQX5VxcQcYN7116IJjMRGkX81QwGYj8CLJhP%252Bca%252BzdfxFeFco9hbHgW8Cz3wlPPeE10T8jZrBaCEV5%252FYsQNYY7eAeKEqZXo%252B4LCEshqZu%252FTW3L57I6mW2IFyV6ruqV8La5nAOCFrwnqIQAGyot4XZUfqa8LaXjW6nmkM7nsYk%253D; fixedview_2689=JALdcwMaXhuy3EI8N1ox%252BnrUGWdpXgy31aZudqWnt%252BxqAY3ZNuaZgacd7anqeBjdZevyPicNCMZgj8l5YbdLPyIyjjY18EQyGDDxg3E6Fa5P9OTTVy8Zo6C9GfaqH0TcSspvNNiAy2wCNtpI65rcwrjdtLmnubML50oPYB8%252Fh2IfxJWG8PeljyzQbJ%252BW4Wf4fh9eSReXOBwqTRO0oNt0EOHpfhn8W523RznOOXG7PvnRoWuGwDNwUeWpZbuNUPAdnBmm%252BnWYPlcVmtGvLK6I009DRiGy5dTXnWuYO1IZvTQCUM%252BtTG2ekz6xHSZ6tuF9cqDOY8r9AjJ0rPqCjQHaDw%253D%253D; fixedview_2690=p8LehnjvUUWOkiSzs9eUo2J5Cii94MbwD3DFYlFJRR53gAzEUTH8PELTN2b%252BwL3agXQA6VLkvTnmMIe52%252FeFNiZYfhhK4xn2YbgloOEMnwO66I%252B36ZJS2Udmh%252BEDGBrp2RSRHG4DstXk5Wo0X5wNdYs69%252FWAEPpSz%252Bq40eDjzQH%252Fe8uNuf9Kng5ffbUBi7XkpNlKyitlUX%252BXaushYbwm9uxcrbilb%252F4oo%252F9%252FpOG1s6Cvo9tubNS8TQWDwl5ah8uVdbTtUVLuQeLDxVJnD%252FkmN0KM2Pd23C%252BpLuaiYt9F0axz6piBSGphdMLiBSxn9fpGiUNDWyq1PCwNXfBSrOYqsw%253D%253D'
}
num = 0
for page in range(16,240):
    data = {
    "did":"2456",
    "sid":"20",
    "tmp":random.random(),
    }
    import time
    time.sleep(1)
    res = requests.request(method='get',url='https://www.qimiaomh.com/Action/Play/AjaxLoadImgUrl?',headers = headers,data=data,verify=False).json()
    list_img = res['listImg'][:-2]
    print(list_img)
    for img in list_img:
        r = requests.request(method='get',url=img,headers = headers,verify=False).content
        with open('photo/{}.jpg'.format(num),'wb')as fp:
            fp.write(r)
            num+=1
