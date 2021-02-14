import urllib.request
import urllib.error
import pickle
from bs4 import BeautifulSoup
import os.path
import datetime

def get_data(url, resultlist):
    try:
        headers = {}
        headers['user-agent'] = r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        req = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')

        # get ball nodes
        soup = BeautifulSoup(html, features="lxml")
        ballnodestr = str(soup.find_all('tbody', id='cpdata')[0]).replace('<tbody id="cpdata">', '').replace('</tbody>', '')
        ballnodes = ballnodestr.split('</tr>')
        for item in ballnodes:
            if item.strip() == '':
                continue
            item = item.strip().replace('<tr>', '')
            itemlist = item.split('</td>')
            if len(itemlist) == 2:
                continue

            term = itemlist[0][5:]
            redball = []
            blueball = []
            cnt = 0
            for ball in itemlist:
                if 'chartball' in ball:
                    cnt += 1
                    ball = int(ball[-2:])
                    if cnt <= 6:
                        redball.append(ball)
                    else:
                        blueball.append(ball)

            # # output to the command line
            # print('下面是第 %s 期双色球开奖结果' % term)
            # print('红色球的结果是:')
            # print(redball)
            # print('蓝色球的结果是:')
            # print(blueball)

            # save to the pickle file
            each_ball_result = {}
            each_ball_result['term'] = term
            each_ball_result['red'] = redball
            each_ball_result['blue'] = blueball
            resultlist.append(each_ball_result)

    except:
        return


def get_top_50():
    url = 'http://match.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=ssq&actionType=chzs&type=50'
    outputfilename = './shuangseqiu.pkl'
    resultlist = []

    get_data(url, resultlist)
    if len(resultlist) == 0:
        return -1
    
    print('正在保存文件....')
    with open(outputfilename, 'wb') as f:
        pickle.dump(resultlist, f)
    
    return 0

def get_all_history():
    # here we want to get the data as much as possible
    # we get data by parameter 'year'
    url = 'http://match.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=ssq&actionType=chzs&year='
    curyear = datetime.datetime.now().year
    if os.path.exists('./dataset.pkl'):
        print('存在')
        olddata = ''
        with open('./dataset.pkl', 'rb') as f:
            olddata = pickle.load(f)
        
        newest_year = olddata[0]['year']
        print(newest_year)
        yearcnt = curyear - newest_year + 1
        olddata.remove(olddata[0])
        for i in range(yearcnt):
            year = newest_year + i
            cururl = url + str(year)
            tmplist = []
            get_data(cururl, tmplist)
            if len(tmplist) == 0:
                return -1
            
            year_dict = {}
            year_dict['year'] = year
            year_dict['data'] = tmplist
            olddata.insert(0, year_dict) 
        
        print('正在保存文件....')
        with open('./dataset.pkl', 'wb') as f:
            pickle.dump(olddata, f)

    else:
        print('不存在')
        yearcnt = 19 # totally save 19 years data online

        # {year: xxxx, data: []}
        dataset = []
        for i in range(yearcnt):
            year = curyear - i
            tmplist = []
            cururl = url + str(year)
            get_data(cururl, tmplist)
            if len(tmplist) == 0:
                return -1
            
            year_dict = {}
            year_dict['year'] = year
            year_dict['data'] = tmplist
            dataset.append(year_dict)

        print('正在保存文件....')
        with open('./dataset.pkl', 'wb') as f:
            pickle.dump(dataset, f)
        
    return 0
            


if __name__ == '__main__':
    get_all_history()