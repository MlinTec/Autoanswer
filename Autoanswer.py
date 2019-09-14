import requests, time, re, random

# 初始化Session对象;
my_headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
# Ses = requests.session()
# Ses.headers = headers

# 登陆教育平台
# @param username(str)
# @param password(str)
def login(userName, passWord):
    url = r'https://henanlogin.xueanquan.com/LoginHandler.ashx?jsoncallback=jQuery161024687563921068412_1566639867210&userName={userName}&password={passWord}&checkcode=&type=login&loginType=1&r={random}&_={time}'.format(userName=userName, passWord=passWord, random=random.random(), time=time.time())
    res = requests.get(url, headers=my_headers)
    userck = res.cookies
    #创建正则，获取用户信息
    rule = 'data:{(.*?)}'
    info = re.findall(rule, res.text)
    #将用户信息存贮在 person_info 字典中
    person_info = {}
    person_info.setdefault('Cookies', userck)
    for infom in info:
        infom = infom.replace('\'','')
        infom_split = infom.split(',')
        for infom_2 in infom_split:
            infom_split_2 = infom_2.split(':')
            person_info.setdefault(infom_split_2[0], infom_split_2[1])
    userinfo = user(**person_info)
    subview(userinfo)

# 构造函数，构造用户信息
class user():
    def __init__(self, **dic):
        self.UserName = dic.get('UserName')
        self.TrueName = dic.get('TrueName')
        self.SchoolID = dic.get('SchoolID')
        self.Grade = dic.get('Grade')
        self.ClassRoom = dic.get('ClassRoom')
        self.PrvCode = dic.get('PrvCode')
        self.CityCode = dic.get('CityCode')
        self.CountryId = dic.get('CountryId')
        self.SchoolName = dic.get('SchoolName')
        self.PrvName = dic.get('PrvName')
        self.CityName = dic.get('CityName')
        self.TownsID = dic.get('TownsID')
        self.ComeFrom = dic.get('ComeFrom')
        self.Cookies = dic.get('Cookies')

def subview(userinfo):
    # 看视频签到
    targetURL = 'https://huodongapi.xueanquan.com/p/henan/Topic/topic/platformapi/api/v1/records/sign'
    data = {"specialId":340,"step":1}
    res = requests.post(targetURL,data=data,headers=my_headers,cookies=userinfo.Cookies)
    print(res.text)
    targetURL = 'https://huodongapi.xueanquan.com/p/henan/Topic/topic/platformapi/api/v1/records/finish-status?specialId=340'
    res = requests.get(targetURL,headers=my_headers,cookies=userinfo.Cookies)
    print(res.text+'----'+userinfo.TrueName)
    # 答题
    '''
    targetURL = 'https://huodongapi.xueanquan.com/Topic/topic/main/api/v1/records/survey'
    data['user']['userName'] = userinfo.UserName
    data['user']['trueName'] = userinfo.TrueName
    data['user']['prvCode'] = userinfo.PrvCode
    data['user']['CityCode'] = userinfo.CityCode
    data['user']['countyId'] = userinfo.CountryId
    data['user']['townId'] = userinfo.TownsID
    data['user']['schoolId'] = userinfo.SchoolID
    data['user']['grade'] = userinfo.Grade
    data['user']['classRoom'] = userinfo.ClassRoom
    data['user']['comeFrom'] = userinfo.ComeFrom
    cookie = userinfo.Cookie.split(';')
    ck_dic = {}
    for item in cookie:
        ck_sp = item.split('=')
        ck_dic.setdefault(ck_sp[0], ck_sp[1])
    '''
    

# 读取txt文本 username----password 内容
filepath = input('Please enter your \'username&password\'txt filepath: ')
# path = C:\Users\Administrator\Desktop\account.txt
with open(filepath, 'r') as f:
    text = f.read()
    text_split = text.split('\n') # 先以 换行符 为分割符对文本进行分割
    for text_i in text_split:
        text_split_2 = text_i.split('----')
        login(text_split_2[0], text_split_2[1])
