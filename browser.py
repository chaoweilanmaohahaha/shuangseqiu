from tkinter import *
from PIL import Image,ImageTk
import pickle
import os.path
from crawlball import *

def get_current_result(term_str, red_ball_str, blue_ball_str):
    res = get_top_50()
    if(res < 0):
        term_str.set('获取失败！')
        return

    file = open('./shuangseqiu.pkl', 'rb')
    result = pickle.load(file)
    file.close()
    term = result[-1]['term']
    term_str.set(term)

    red_balls = result[-1]['red']
    for i in range(len(red_balls)):
        red_ball_str[i].set(str(red_balls[i]).rjust(2, '0'))

    blue_ball = result[-1]['blue'][0]
    blue_ball_str.set(str(blue_ball).rjust(2, '0'))

def subwindow():
    window = Tk()
    # window.geometry('400x400')
    window.title('浏览过往50期结果')

    if not os.path.exists('shuangseqiu.pkl'):
        print('点击一下获取最新一期号码来获取信息吧！')

    res = ''
    with open('shuangseqiu.pkl', 'rb') as f:
        res = pickle.load(f)
    
    size = len(res)
    for i in range(5):
        label1 = Label(window, text = '期号')
        label1.grid(row = 0, column = i*3 + 0)
        label2 = Label(window, text = '红色球')
        label2.grid(row = 0, column = i*3 + 1)
        label3 = Label(window, text = '蓝色球')
        label3.grid(row = 0, column = i*3 + 2)

        for j in range(10):
            termlabel = Label(window, text = res[-(i*10+j+1)]['term'])
            termlabel.grid(row = j+1, column = i*3 + 0)

            redstr = ''
            for item in res[-(i*10+j+1)]['red']:
                redstr += str(item).rjust(2, '0') + ' '
            redlabel = Label(window, text = redstr, fg = 'red')
            redlabel.grid(row = j+1, column = i*3 + 1)

            bluelabel = Label(window, text = str(res[-(i*10+j+1)]['blue'][0]).rjust(2, '0'), fg = 'blue')
            bluelabel.grid(row = j+1, column = i*3 + 2)
    
    # scroll_bar = Scrollbar(canvas, orient=VERTICAL)
    # scroll_bar.pack(side=RIGHT, fill = Y)
    # scroll_bar.configure(command=canvas.yview)
    # canvas.config(yscrollcommand=scroll_bar.set)

    window.mainloop()

    

def get_history(term_str):
    res = get_all_history()
    if(res < 0):
        term_str.set('下载失败！')
    else:
        term_str.set('下载完毕！')        
    
def main():
    browser = Tk()
    browser.title('我的双色球浏览器')

    frame1 = Frame(browser, bg = 'white')
    frame2 = Frame(browser)

    redpic = Image.open('./red.png')
    bluepic = Image.open('./blue.png')
    redpic = redpic.resize((100, 100))
    bluepic = bluepic.resize((100, 100))
    redbg = ImageTk.PhotoImage(redpic)
    bluebg = ImageTk.PhotoImage(bluepic)

    red_ball_str = []
    for i in range(6):
        new_str = StringVar()
        red_ball_str.append(new_str)
        
        new_label = Label(frame1,
                        textvariable = red_ball_str[i],
                        image = redbg,
                        compound=CENTER,
                        fg='white',
                        font=('楷体', 50))
        new_label.grid(row = 0, column = i)

    blue_ball_str = StringVar()
    blue_ball_label = Label(frame1,
                            textvariable = blue_ball_str,
                            image = bluebg,
                            compound=CENTER,
                            fg='white',
                            font=('楷体', 50))
    blue_ball_label.grid(row = 0, column = 6)


    frame1.pack()

    term_str = StringVar()
    term_label = Label(browser,
                    textvariable = term_str,
                    font=('楷体', 20),
                    compound=CENTER,
                    fg='black')
    term_label.pack()

    button1 = Button(frame2, text = '查看最新一期', command = lambda :get_current_result(term_str, red_ball_str, blue_ball_str))
    button2 = Button(frame2, text = '查看历史记录', command = subwindow)
    button3 = Button(frame2, text = '下载历史数据', command = lambda :get_history(term_str))

    button1.grid(row = 0, column = 0, padx = 8, pady = 2)
    button2.grid(row = 0, column = 1, padx = 8, pady = 2)
    button3.grid(row = 0, column = 2, padx = 8, pady = 2)
    frame2.pack()

    browser.mainloop()

if __name__ == '__main__':
    main()