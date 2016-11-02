from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

# 根据网址获取一个网页内容，返回BeautifulSoup对象
def openWebPage(url):
    try:
        print('打开网页%s: ' % url)
        html = urlopen(url)
        bsObj = BeautifulSoup(html)
        print('打开网页%s成功' % url)
        return bsObj
    except:
        print('打开网页%s时发生错误' % url)
        return None

# 
def getInfosInAPage(bsObj):
    try:
        lis = bsObj.find('ul', {'id': 'house-lst'}).find_all('li')
    except:
        print('无法获取id为house-lst的ul，请检查')
    infos = []
    for li in lis:
        #print('----------------------------------------------------')
##        print(li)
        info = getInfosInALi(li)
        infos.append(info)
        #print('---------------------------------------------------')
    return infos
        

def getInfosInALi(li):
    infos = {}
    address = ''
    ceng = ''
    chaoXiang = ''
    year = ''
    leiXing = ''
    area = ''
    totalPrice = ''
    averagePrice = ''
    try:
        infoPanel = li.find('div', {'class': 'info-panel'})
        infos['标题'] = infoPanel.h2.a.get_text()
        #print(infos['标题'])
        
        info = infoPanel.find('div', {'class': 'other'}).get_text().replace('\t', '').replace('\n','').split('|')
        #print(info)
        address += info[0]
        ceng = info[1].replace('\r', '')
        infos['层数'] = ceng
        if(len(info) >= 3):
            chaoXiang = info[2].replace('\r', '')
        infos['朝向'] = chaoXiang
        if(len(info) == 4):
            year = info[3].replace('\r', '')
        infos['建成年份'] = year
        #print(infos)
            
        info = infoPanel.find('div', {'class': 'where'}).get_text().replace('\xa0',' ').replace('\r', '').replace('\t', '').lstrip().rstrip().replace('\n', '').split(' ')
        #print(info)
        address += info[0]
        infos['地址'] = address
        leiXing += info[2]
        infos['户型'] = leiXing
        area += info[4]
        infos['面积'] = area
        #print(infos)

        totalPrice = infoPanel.find('div', {'class': 'price'}).span.get_text()
        infos['总价'] = totalPrice
        averagePrice = infoPanel.find('div', {'class': 'price-pre'}).get_text()[0:-3]
        infos['均价'] = averagePrice
        #print(infos)
        return infos
    except:
        print('获取房屋信息出错')
        print(infos)
        return infos


#
def saveInfosIntoCSV(infos, path):
    try:
        print('开始保存信息')
        csvFile = open(path, 'a+', newline='')
        writer = csv.writer(csvFile)
##        writer.writerow(['标题', '地址', '户型', '朝向', '层数', '建成年份', '面积', '总价', '均价'])
        for info in infos:
            row = []
            row.append(info['标题'])
            row.append(info['地址'])
            row.append(info['户型'])
            row.append(info['朝向'])
            row.append(info['层数'])
            row.append(info['建成年份'])
            row.append(info['面积'])
            row.append(info['总价'])
            row.append(info['均价'])
            writer.writerow(row)
        csvFile.close()
        print('保存信息完成')
    except:
        print('保存信息出错')

def writeHeaderIntoCSV(header, path):
    csvFile = open(path, 'a+', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(header)
    csvFile.close()
    

if __name__ == '__main__':
    baseUrl = 'http://sh.lianjia.com/ershoufang/d'
    length = 0
    temp = 0
    fileIndex = 1
    index = 1
    results = []
    writeHeaderIntoCSV(['标题', '地址', '户型', '朝向', '层数', '建成年份', '面积', '总价', '均价'], 'D:\\python爬虫\\链家网(上海)\\LianJia' + str(fileIndex) + '.csv')
    while True:
        url = baseUrl + str(index)
        bsObj = openWebPage(url)
        if(bsObj == None):
            break
        results += getInfosInAPage(bsObj)
        length += len(results)
        temp += len(results)
        saveInfosIntoCSV(results, 'D:\\python爬虫\\链家网(上海)\\LianJia' + str(fileIndex) + '.csv')
        if(temp > 100000):
            temp = 0
            fileIndex += 1
        index += 1
    print('===================================================================================================')
    print(length)

##    url = 'http://sh.lianjia.com/ershoufang/d785'
##    bsObj = openWebPage(url)
##    if(bsObj != None):
##        print(getInfosInAPage(bsObj))
    
