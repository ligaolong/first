# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import subprocess,os,sys,time
globalStartupInfo = subprocess.STARTUPINFO()
globalStartupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
from bottle import route, run


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        # print('click', event)
        # print('【button=%d, x=%d, y=%d, xdata=%f, ydata=%f】' %
        #       (event.button, event.x, event.y, event.xdata, event.ydata))
        print(event.xdata, event.ydata)
        # fig.canvas.mpl_disconnect(self.cid) #停止鼠标响应事件
        x = str(event.xdata)
        y = str(event.ydata)
        x, dx = x.split(".")
        y, dy = y.split(".")
        print('------------')
        print(x, y)
        plt.close()
        cli = 'adb  -s ' + xuliehao + '  shell input tap '+x+' '+y
        print(cli)
        runCmd(cli)
        auto_xy()

def runCmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd(), shell=False, startupinfo=globalStartupInfo)
    p.wait()
    re=p.stdout.read().decode()
    return re
def conn_phone():
    #连接的手机列表
    mobiles=[]
    cmd=['adb','devices']
    mobilelist=runCmd(cmd)
    mobilelist=mobilelist.split('\r\n')[1:]
    # print(mobilelist)
    for x in mobilelist:
        if x:
            mobiles.append(x)
    if mobiles:
        print(mobiles)
    else:
        print(['no devices\t no devices'])
    #取第一个手机的序列号
    global xuliehao
    if mobiles:
        #取第一个手机设备
        device=mobiles[0].split('\t')
        xuliehao=device[0]
        print(device)
    #有手机连接上就截图
    if xuliehao:

        #打开用钱宝APP
        s = runCmd('adb  -s ' + xuliehao + '  shell am start com.yongqianbao.credit/com.yongqianbao.credit.activites.SplashActivity')
        time.sleep(15)
        # 点击左上角
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 38 70')
        time.sleep(1)
        # 点击已有账号去登录
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 102 534')
        time.sleep(2)
        # 点击输入手机号
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 173 332')
        time.sleep(2)
        # 输入手机号
        s = runCmd('adb  -s ' + xuliehao + '  shell input text 13661176390')
        time.sleep(2)
        # 点击输入密码
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 192 358')
        time.sleep(2)
        # 输入密码
        s = runCmd('adb  -s ' + xuliehao + '  shell input text qq1253151')
        time.sleep(2)
        # 点击登录
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 270 468')
        #截图
        auto_xy()
        # 点击左上角
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 35 78')
        time.sleep(1)
        # 点击借款记录
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 129 464')
        time.sleep(1)
        #截图
        auto_xy()
        # 点击返回
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 40 76')
        time.sleep(1)
        # 点击头像
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 222 118')
        time.sleep(1)
        # 点击退出
        s = runCmd('adb  -s ' + xuliehao + '  shell input tap 325 500')
        time.sleep(15)
    else:
        print('no device!')

def auto_img():
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    jietupath = 'E://pics'
    sdcardpath = '/sdcard/screenshot-' + timestamp + '.png'
    if not os.path.exists(jietupath):
        os.makedirs(jietupath)
    jietupath += '/screenshot-' + timestamp + '.png'
    # os.remove(jietupath)
    print('it is screenshoting to mobile.....')
    jtcmd = 'adb   -s ' + xuliehao + ' shell /system/bin/screencap -p ' + sdcardpath
    # print(jtcmd)
    result = runCmd(jtcmd)
    print('it is screenshot success.....')
    # print(result)
    print('it is moving screenshot to pc.....')
    jtcmd = 'adb  -s  ' + xuliehao + ' pull ' + sdcardpath + ' ' + jietupath
    # print(jtcmd)
    result = runCmd(jtcmd)

    # print(result)
    # 删除sd图片
    jtcmd = 'adb -s ' + xuliehao + ' shell rm  ' + sdcardpath
    # print(jtcmd)
    result = runCmd(jtcmd)
    print(result)
    print('it is moved screenshot to pc success.....')
    return jietupath

def auto_xy():
        time.sleep(5)
        end_path = auto_img()
        image_file = cbook.get_sample_data(end_path)
        image = plt.imread(image_file)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(image)
        line, = ax.plot([0], [0])  # empty line
        xy = LineBuilder(line)
        plt.show()
if __name__ =="__main__":
    conn_phone()

# #支付二维码：
# def test():
#     imgSuccess = 'adb - s'+ xuliehao +'shell rm '
# @route('/test')#word简历搜索的关键字
# def index():
#     conn_phone()
# run(port=8080, host='localhost')
