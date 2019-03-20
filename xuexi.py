from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

import plusTime
##import pageAccess

        

def scroll(dr,seconds):
        j = round(seconds/10) ##滚动页面10次
        for x in range(j):
                time.sleep(10)  
                xOffset = random.randint(0,100)
                yOffset = random.randint(0,200)
                js = 'window.scrollTo('+str(xOffset)+','+ str(yOffset) + ')'
                print('正在浏览网页，第'+str(x)+'次延时，共延时了'+str(x*10)+'秒')
                if fDebug :                        
                        print(js)
                dr.execute_script(js)

def toNewWnd():
    ##新建窗口并跳转
    hOld = dr.current_window_handle
    dr.execute_script('window.open()')
    dr.switch_to.window(dr.window_handles[-1])
    return hOld
    
def getScore():
    hOld = dr.current_window_handle
    dr.switch_to.window(hScore)
    
    dr.refresh()
    time.sleep(5)
    items = dr.find_elements_by_xpath('//div[@class="my-points-card-text"]')
    strArticles = items[1].text
    strVideos = items[2].text
    strArticleTime = items[3].text
    strVideoTime = items[4].text
    print(' 文章数:'+strArticles+' 视频数:'+strVideos+' 文章时长:'+strArticleTime+' 视频时长:'+strVideoTime)
    
    dr.switch_to.window(hOld)
    
    if fDebug == True:
            print('3'+dr.title)
    i1= int(strArticles[0])
    i2 = int(strVideos[0])
    i3 = int(strArticleTime[0])
    if len(strVideoTime)==6 :
       i4 = int(strVideoTime[0])
    else:
       i4 = int(strVideoTime[0:2])
    score = [i1,i2,i3,i4]       
    return score
    
    
def getDuration():
    time.sleep(5)
    bar = dr.find_elements_by_xpath('//div[@class="prism-controlbar"]')
    if len(bar)==0:
            return -1  ##不是视频页面
    js = 'document.getElementsByClassName("prism-controlbar")[0].style.display="block"'
    dr.execute_script(js)    
    duration = dr.find_element_by_xpath('//span[@class="duration"]').text
    m = int(duration[0:2])
    s = int(duration[3:5])
    print('视频长度：%d分钟%s秒钟' %(m,s))
    return m*60+s
    
def lianbo():    
    print('开始观看新闻联播')
    hOld = toNewWnd()
    
    dr.get(myurls['重要活动视频'])
    labels = dr.find_elements_by_xpath('//label')
    labels[-1].click()
    items = dr.find_elements_by_xpath('//div[@class="word-item"]')
    hList = dr.current_window_handle
    
    items[0].click()
    hs = dr.window_handles
    dr.switch_to.window(hs[-1])
    if fDebug == True:
            duration = getDuration()
    while isTaskOk(Task['视频时长']) == False:
            print('视频时长未达标，延时360秒')
            if fActiveTime == True :
                    scroll(dr,300+30)
            else:
                    scroll(dr,150+30)
    print('视频时长已达标')    
    dr.close()
    dr.switch_to.window(hList)
    
    dr.close()
    dr.switch_to.window(hOld)
    print('新闻联播观看完毕')
    

def surfArticle(urlList):
                      
        print('开始浏览文章')
        hOld  = toNewWnd()
        dr.get(myurls[urlList])

        hs = dr.window_handles
        dr.switch_to.window(hs[-1])        
        hBase = dr.current_window_handle
        
        time.sleep(5)
 
        items = dr.find_elements_by_xpath('//div[@class="word-item"]')
        print('现在进入 '+dr.title+' 目录')  
                      
        i=0
        while isTaskOk(Task['文章数']) == False:
                print('文章篇数未达标')
                items[i*2].click()
                hs = dr.window_handles
                dr.switch_to.window(hs[len(hs)-1])
                print('浏览第'+str(i+1)+'个链接')
                print('链接名称：'+dr.title)
                scroll(dr,120)
                print('当前主页： '+ dr.title)                        
                dr.close()
                dr.switch_to.window(hBase)
                print('当前主页：  '+ dr.title)
                i+=1

        print('当前主页：  '+ dr.title)
        print('文章篇数已达标')

        ##最后一篇文章用于时长达标
        if isTaskOk(Task['文章时长']) == False :
                print('文章时长未达标,开始赚时长')                            
                items[i*2].click()
                hs = dr.window_handles
                dr.switch_to.window(hs[len(hs)-1])
                iArticleTime = getScore()[2]
                while iArticleTime<8 :
                        print('延时240秒')
                        if fActiveTime == True :
                                scroll(dr,120+30)
                        else:
                                scroll(dr,240+30)
                        iArticleTime = getScore()[2]
                        print('文章时长：'+str(iArticleTime)+'/8')                     
                        
                dr.close()
                dr.switch_to.window(hBase)
        print('当前主页：  '+ dr.title)        
        print('文章时长已达标')        

        dr.close()
        dr.switch_to.window(hOld)
        
def surfVideo(urlList):


        if isTaskOk(Task['视频数']) == True :
                print('视频数已达标')
                return
        print("开始观看视频")
        hOld  = toNewWnd()
        dr.get(myurls[urlList])
        hs = dr.window_handles
        dr.switch_to.window(hs[len(hs)-1])        
        hBase = dr.current_window_handle        
##        items = dr.find_elements_by_xpath('//li[@class="num"]')
##        items[len(items)-1].click()         

        
        time.sleep(5)
        print('现在进入 '+dr.title+' 目录')    
        items = dr.find_elements_by_xpath('//div[@class="word-item"]')
    
        i=1
        while isTaskOk(Task['视频数']) == False:
                items[i*2].click()
                hs = dr.window_handles
                dr.switch_to.window(hs[len(hs)-1])
                print('浏览第'+str(i)+'个链接')
                print('链接名称：'+dr.title)
                scroll(dr,getDuration())  
                dr.close()
                dr.switch_to.window(hBase)
                i+=1

        print('视频数已达标')
        
        if isTaskOk(Task['视频时长']) == False :
                print('视频时长未达标')
                lianbo()
        print('视频时长已达标')         
        dr.close()
        dr.switch_to.window(hOld)
        
def surfLocal(urlList)
        hOld  = toNewWnd()     

        dr.get(urlList)
        print("打开地方平台页面")
        time.sleep(5)
        hList = dr.current_window_handle        
        links = dr.find_elements_by_xpath('//div[@class = "ant-row-flex"]/div/div/div/ul/li/span')           
        if fDebug :print("获取资源链接列表")
        cItem = len(items)
        if fDebug :print("获取%d个链接" %cItem)
        j=0
        cReadedA = 0
        cReadedV = 0
        while isTaskOk(Task['文章数']) == False:
                print('文章篇数未达标')
                while j<cItem:
                        links[j].click()
                        hs = dr.window_handles
                        dr.switch_to.window(hs[len(hs)-1])
                        print('浏览第%d个链接' %j)
                        print('链接名称：'+dr.title)
                        if len(links[j].find_elements_by_xpath('./i'))==1:
                                print('本链接是视频页面')
                                scroll(dr,getDuration())
                                playIcon = dr.find_element_by_xpath('//div[@class="outter"]')
                                playIcon.click()
                                cReadedV+=1
                        else:
                                print('本链接是文字链接')                                
                                scroll(dr,120)
                                cReadedA+=1
                        dr.close()
                        dr.switch_to.window(hList)
        dr.close()
        dr.switch_to.window(hOld)
        
def isTaskOk(iTask):

        if fDebug == True:
            print('4'+dr.title)
            
        time.sleep(3)
        print('延时3秒，等待积分更新')
        if iTask == 0:
                if getScore()[iTask]==6:
                        return True
        elif iTask == 1:
                if getScore()[iTask]==6:
                        return True
        elif iTask == 2:
                if getScore()[iTask]==8:
                        return True    
        elif iTask == 3:
                if getScore()[iTask]==10:
                        return True
        return False
      

##fActive
##hScore
articleUrls = {
          ##文章
          '学习新思想':'https://www.xuexi.cn/cc72a0454287bdedb7e2c156db55e818/71eb7214c6c0c1f5e6ec6e29564decb4.html',
          '重要新闻':'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html',
          '综合新闻':'https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html',
          '新闻发布厅':'https://www.xuexi.cn/bab787a637b47d3e51166f6a0daeafdb/9a3668c13f6e303932b5e0e100fc248b.html',
          '中宣部发布':'https://www.xuexi.cn/105c2fa2843fa9e6d17440e172115c92/9a3668c13f6e303932b5e0e100fc248b.html',
          '头条新闻':'https://www.xuexi.cn/72ac54163d26d6677a80b8e21a776cfa/9a3668c13f6e303932b5e0e100fc248b.html',
          '学习时评':'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html',
          '学习实践':'https://www.xuexi.cn/03c8b56d5bce4b3619a9d6c2dfb180ef/9a3668c13f6e303932b5e0e100fc248b.html'
        }

myurls = {
          ##功能页
          '登录':'https://pc.xuexi.cn/points/login.html?ref=https://www.xuexi.cn/cc72a0454287bdedb7e2c156db55e818/71eb7214c6c0c1f5e6ec6e29564decb4.html',
          '积分':'https://pc.xuexi.cn/points/my-points.html',
          ##文章
          '重要新闻':'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html',
          '综合新闻':'https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html',
          '新闻发布厅':'https://www.xuexi.cn/bab787a637b47d3e51166f6a0daeafdb/9a3668c13f6e303932b5e0e100fc248b.html',
          '中宣部发布':'https://www.xuexi.cn/105c2fa2843fa9e6d17440e172115c92/9a3668c13f6e303932b5e0e100fc248b.html',
          '头条新闻':'https://www.xuexi.cn/72ac54163d26d6677a80b8e21a776cfa/9a3668c13f6e303932b5e0e100fc248b.html',
          '学习时评':'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html',
          '学习实践':'https://www.xuexi.cn/03c8b56d5bce4b3619a9d6c2dfb180ef/9a3668c13f6e303932b5e0e100fc248b.html',
          '重要新闻':'https://www.xuexi.cn/98d5ae483720f701144e4dabf99a4a34/5957f69bffab66811b99940516ec8784.html',##此版块更新较多，提高被选中概率
          '综合新闻':'https://www.xuexi.cn/7097477a9643eacffe4cc101e4906fdb/9a3668c13f6e303932b5e0e100fc248b.html',##此版块更新较多，提高被选中概率
          ##视频
          '学习电视台':'https://www.xuexi.cn/0809b8b6ab8a81a4f55ce9cbefa16eff/ae60b027cb83715fd0eeb7bdr527e88b.html',          
          '新闻联播':'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html',
          '重要活动视频':'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html',
          '学习研究':'https://www.xuexi.cn/3695ce40a2f38ca24261ee28953ce822/9a3668c13f6e303932b5e0e100fc248b.html',
        }
Task = {'文章数':0,
        '视频数':1,
        '文章时长':2,
        '视频时长':3,
        }

co = Options()
co.add_argument('--headlesss')
co.add_argument("--silent")
dr = webdriver.Chrome(options = co)

import urls

##fDebug = False          
##fActiveTime = plusTime.isPlusTime()

##//a[contains(text(),"查看更多")]
dr.get(urls.avUrls['北京映象'])
hList = dr.current_window_handle
time.sleep(5)
items = dr.find_elements_by_xpath('//div[@class = "ant-row-flex"]/div/div/div/ul/li/span')
j = len(items)
fVUrl = []
t = []
for i in items:
        dr.title
        if len(i.find_elements_by_xpath('./i'))==1:
                fVUrl.append(True) ##span标签下有i标签即播放按钮图标，本链接是视频链接
                hOld = dr.current_window_handle
                i.click()
                dr.switch_to.window(dr.window_handles[-1])
                t.append(getDuration())
                dr.close()
                dr.switch_to.window(hOld)
        else:
                fVUrl.append(False)              
                
        pass ##延时
        
        






##dr.set_window_size(300,500)
##for i in range(10):
##	random.sample(articleUrls.keys(),1)
##for i in articleUrls:
##        dr.get(articleUrls[i])
##        print(dr.title)
##        items = dr.find_elements_by_xpath('//div[@class="word-item"]')
##        for it in items:
##                print(it.text)
##        input("pause")



##dr.get(myurls['登录'])
##
##dr.execute_script('window.scrollTo(500,900)')
##input('登录成功，请按回车')
##
##
##dr.get(myurls['积分'])
##hScore = dr.current_window_handle

##surfArticle('重要新闻')
##surfVideo('重要活动视频')







