from os import listdir,walk,path,system
from tkinter import Tk,Button,Entry,Label,Text,Frame,END
import datetime
from time import strftime,localtime
from collections import Counter
import calendar,re

class User:
    def __init__(self):
        pass

    def user_file(self,name):
        names_list = listdir('.\\data')
        if (name + '.txt')  not in names_list:
            f =  open('.data\\' + name + '.txt','a')
            f.close()
        file_name = name + '.txt' 
        return file_name

    def load_conf(self):
        global user_command
        conf_dir = '.\\config\\diary.conf'
        f = open(conf_dir,'r')
        user_command = f.readlines()   
        return user_command


class Application():
    def __init__(self,master):
        self.root = master


        initface(self.root)

class initface():
    def __init__(self,master):
        global currenttime
        currenttime = strftime('%Y-%m-%d %H:%M:%S',localtime()).split(' ')
        self.Year = int(currenttime[0].split('-')[0])
        self.Month = int(currenttime[0].split('-')[1])
        self.Day = int(currenttime[0].split('-')[2])
        self.master = master
        self.user_info = User()
        #设置窗口大小和位置
        self.master.geometry('370x400+400+100')
        self.master.minsize(370,400)
        self.master.maxsize(370,400)
        self.master.title(u'我的成功日记')
        global content_first
        command = self.user_info.load_conf()
        #print(command)

        #创建一个文本框
        #self.entry = Entry(self.master)
        #self.entry.place(x=10,y=10,width=200,height=25)
        #self.entry.bind("<Key-Return>",self.submit1)
        self.record_in = Text(self.master,background = 'azure')
        # 喜欢什么背景色就在这里面找哦，但是有色差，得多试试：http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
        self.record_in.place(x = 10,y = 5,width = 345,height = 155)
        self.record_in.bind("<Key-Return>",self.submit1)

        #创建三个按钮
        #为按钮添加事件
        #self.submit_btn = Button(self.master,text=u'提交',command=self.submit)
        #self.submit_btn.place(x=280,y=165,width=35,height=25)
        self.submit_btn2 = Button(self.master,text=u'复位',command = self.reset)
        self.submit_btn2.place(x=200,y=365,width=40,height=30)
        self.submit_btn3 = Button(self.master,text=u'保存上传',command = self.upload)
        self.submit_btn3.place(x=280,y=365,width=65,height=30)
        self.submit_btn4 = Button(self.master,text=u'查看日历',command = self.check)
        self.submit_btn4.place(x=20,y=365,width=65,height=30)
        #日记记录输出结果
        self.title_label = Label(self.master,text=u'diary record:')
        self.title_label.place(x=10,y=165)
        #记录结果

        self.record_out = Text(self.master,background = 'light cyan')
        self.record_out.place(x = 10,y = 193,width = 345,height = 165)
        #回车提交

        #初始参数输入
        self.record_in.insert(END,'请输入用户名：')
        self.record_in.focus_force()
        #self.record_in.mark('insert',END)
        #print(currenttime)
        #print(currenttime)
        content_first = '日期： ' + currenttime[0] + '     时间： ' + currenttime[1] + '\n'
        self.record_out.insert(END,content_first)

    def check(self):
        global datelist,cmd_index,file_name,user_command,backupdir
        backupdir = user_command[-1].split(' ')[1]
        #print(backupdir)
        cmd_index = 0
        datelist = []
        if file_name == '':
            datelist = []
        else:
            with open('.\\data\\' + file_name + '.txt',"r") as f:
                data = f.read()
                #print(data)
            date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",data)
            for date in date_all:
                datelist.append(date)
        #print(datelist)

        self.record_in.destroy()
        self.record_out.destroy()
        self.submit_btn2.destroy()
        self.submit_btn3.destroy()
        self.submit_btn4.destroy()
        self.title_label.destroy()
        Calendar_ui(self.master,self.Year,self.Month,self.Day)
        
    def submit1(self,event):
        global cmd_index
        global user_command
        global file_name
        #从输入框获取用户输入的值
        #content_ori = self.result_text1.get(0.0,END).split('\n')[-2]
        #print(content_ori)
        #content = content_ori.strip().replace("\n"," ")
        content = self.record_in.get(0.0,END)
        self.user_name = content.strip().replace('\n','').split('：')[-1]
        #print(content)
        if cmd_index == 0:
            self.record_out.insert(END,'你好，' + self.user_name + '\n\n')
            file_name = self.user_name
        else:
            self.record_out.insert(END,content.strip() + '\n')

        self.record_in.delete(0.0,END)
        self.record_in.mark_set('insert','0.0')

        cmd_index += 1
        #print(user_command)
        if cmd_index <= len(user_command)-1:
            self.record_in.insert(0.0,user_command[cmd_index - 1].strip().replace('\n',''))
        else:
            self.record_in.mark_set('insert','0.0')
            self.record_in.insert(0.0,'当天的成功日记已经完成，请确认内容后点击‘保存上传...’')
        
        #self.result_text.delete(0.0,END)
        #self.result_text.insert(END,result)

        #print(content)

    def reset(self):
        global cmd_index
        self.record_in.delete(0.0,END)
        self.record_out.delete(2.0,END)
        self.record_out.insert(END,'\n')
        self.record_in.insert(END,'请输入用户名：')
        cmd_index = 0


    def upload(self):
        global content_first
        if file_name != '':
            self.record_in.delete(0.0,END)
            self.record_in.mark_set('insert','0.0')
            f =  open('.\\data\\' + file_name + '.txt','a+')
            record = self.record_out.get(0.0,END).strip() + '\n\n\n\n\n'
            f.write(record)
        else:
            self.record_in.insert(0.0,'未指定用户名，请按复位键！')
        f.seek(0)
        lines = f.readlines()
        #print(Counter(lines)[content_first])
        if Counter(lines)[content_first] == 0:
            self.record_in.insert(0.0,'保存失败！')
        elif Counter(lines)[content_first] == 1:
            self.record_in.insert(0.0,'保存成功！')
        elif Counter(lines)[content_first] > 1:
            self.record_in.insert(0.0,'存在重复上传数据，可进入文件删除多余内容！')
        f.close()


class Calendar_ui():
    def __init__(self,master,Year,Month,Day):
        global datelist,file_name,currenttime
        self.master = master
        self.master.title(u'日历')
        self.master.geometry('440x500+400+100')
        self.master.minsize(440,500)
        self.master.maxsize(440,500)
        self.Year = Year
        self.Month = Month
        self.Day = Day

        #print(self.Year)
        #print(self.Month)
        #print(self.Day)

        self.button1 = Button(self.master, text='Previous',width =8,height = 1, command=self.ButtonPrevious)
        self.button1.place(x=50,y=240,width=80,height=30)
        self.button2 = Button(self.master, text='Next',width =8,height = 1, command=self.ButtonNext)
        self.button2.place(x=150,y=240,width=80,height=30)
        self.button3 = Button(self.master, text='back diary',width =8,height = 1, command=self.Back)
        self.button3.place(x=340,y=240,width=80,height=30)
        self.button4 = Button(self.master,text=u'查看日记',command = self.review)
        self.button4.place(x=340,y=400,width=80,height=30)
        self.button5 = Button(self.master,text=u'日记备份',command = self.backup)
        self.button5.place(x=340,y=450,width=80,height=30)
        self.summary_log = Text(self.master,background = 'azure')
        self.summary_log.place(x = 20,y = 280,width = 310,height = 200)
        self.summary_log.bind("<Key-Return>",self.enter)
        self.summary_log.delete(0.0,END)
        self.summary_log.insert('0.0','---绿底日期代表当天有日记记录。')
        if file_name == '':
            self.summary_log.insert(END,'\n---还未输入用户名，请返回日记界面输入有效的日记用户名')
        else:
            self.summary_log.insert(END,'\n---首次记录成功日记时间为： %s。'% datelist[0])
            now = datetime.datetime.strptime(currenttime[0],"%Y-%m-%d")
            firstday = datetime.datetime.strptime(datelist[0],"%Y-%m-%d")
            days = (now-firstday).days
            #print(days)
            self.summary_log.insert(END,'\n---距今天数： %d天,  '% days)
            now_rate= (len(datelist))/days
            #print(now_rate)
            self.summary_log.insert(END,'准时完成度： {:.1f}%。'.format(now_rate*100))
        self.ui_update()


    def ui_update(self):
        global file_name,datelist,currenttime
        #print(datelist)
        #print(self.Month)
        # 首行放置“年、月”的位置
        label = Label(self.master,text= str(self.Year) +"年")
        label.grid(row=0,column=2)
        label = Label(self.master,text= str(self.Month) +"月")
        label.grid(row=0,column=4)
        # labels列表：放置“星期”的标题
        # 用calendar库计算日历
        #global MonthCal

        labels = [['Mon','Tue','Wed','Thu','Fri','Sat','Sun']]
        self.MonthCal = calendar.monthcalendar(self.Year, self.Month)
        days_in_month = calendar.monthrange(self.Year,self.Month)[1]
        #print(days_in_month)

        #for days_in_week in self.MonthCal:
            #days_in_month = days_in_month + days_in_week
        #print(max(days_in_month))

        if self.Month < 10:
            select_month= str(self.Year) + '-0' + str(self.Month)
        else:
            select_month= str(self.Year) + '-' + str(self.Month)
        
        self.dayslist_inMonth = []
        for days in datelist:
            #print(select_month)
            #print(days)
            if re.match(select_month,days) != None:
                self.dayslist_inMonth.append(days)
           
        #print(dayslist_inMonth)

        #print(self.MonthCal)
        self.clear_grid()
        # 把日历加到labels列表中     
        for i in range(len(self.MonthCal)):
            labels.append(self.MonthCal[i])
        #print(self.labels)
        # 放置日历
        for r in range(len(self.MonthCal)+1):
            for c in range(7):
                if labels[r][c] == 0:
                    labels[r][c] = ' '
                if (r == 0) or (labels[r][c] == ' '):
                    label = Label(self.master,
                                    width =7,
                                    padx=4,
                                    pady=5,
                                    justify ='center',
                                    text=str(labels[r][c]))     

                else:
                    date_string= datetime.date(self.Year,self.Month,int(labels[r][c]))
                    #print(date_string)
                    #print(datelist)
                    if str(date_string) in datelist:
                        label = Label(self.master,
                                        bg = 'green',
                                        width =7,
                                        padx=4,
                                        pady=5,
                                        justify ='center',
                                        text=str(labels[r][c])) 
                        #print('yes')
                    else:
                        label = Label(self.master,
                                        #bg = 'yellow',
                                        width =7,
                                        padx=4,
                                        pady=5,
                                        justify ='center',
                                        text=str(labels[r][c])) 
                        #print('no')
                 
                label.grid(row=r+1,column=c) # 网格布局

        if file_name != '':
            month_rate = len(self.dayslist_inMonth)/days_in_month
            self.summary_log.insert(END,'\n---{}月完成度： {:.1f}%。'.format(self.Month,month_rate*100))


    def clear_grid(self):
        # 先把界面清空
        for r in range(7):
            for c in range(7):            
                label = Label(self.master,
                              width =7,
                              padx=4,
                              pady=5,
                              justify ='center',
                              text=' ')        
                label.grid(row=r+1,column=c)


    # button：Enter
    def ButtonPrevious(self):
        self.Month = self.Month-1
        if self.Month<1:
            self.Month = self.Month+12
            self.Year = self.Year-1
        self.ui_update()


    # button：Clear
    def ButtonNext(self):
        self.Month = self.Month+1
        if self.Month>12:
            self.Month = self.Month-12
            self.Year = self.Year+1 
        self.ui_update()

    def Back(self):
        global file_name
        self.clear_grid()
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.summary_log.destroy()
        self.button4.destroy()
        self.button5.destroy()
        file_name = ''
        initface(self.master)

    def review(self):
        self.summary_log.delete(0.0,END)
        if self.Month < 10:
            self.summary_log.insert(END,'---请输入需要查阅的日期： {}-0{}-'.format(str(self.Year),str(self.Month)))
        else:
            self.summary_log.insert(END,'---请输入需要查阅的日期： {}-{}-'.format(str(self.Year),str(self.Month)))
        self.summary_log.focus_force()



    def enter(self,event):
        self.dialog = False
        infor_insert = self.summary_log.get(0.0,END)
        last_line = infor_insert.split('---')[-1]
        #print(last_line)
        date_an = last_line.split(' ')[-1].split('-')

        try:
            if int(date_an[2]) < 10:
                self.date_select = '{}-{}-0{}'.format(date_an[0],date_an[1],date_an[2])
            elif int(date_an[2]) < 31:
                self.date_select = '{}-{}-{}'.format(date_an[0],date_an[1],date_an[2])
            else:
                self.summary_log.insert(END,'\n---输入错误，日期应小于31！')
                self.summary_log.insert(END,'\n- - - - - - - - - - - - - - - - - - - - - -\n')
                self.dialog = True
            #print(date_select)
        except ValueError:
            self.summary_log.insert(END,'\n---输入的值不正确，请重新输入日期！')
            self.summary_log.insert(END,'\n- - - - - - - - - - - - - - - - - - - - - -\n')
            self.dialog = True

        try:
            if self.dayslist_inMonth.count(self.date_select.replace('\n','')) == 1: 
                pass
            else:
                #print(len(self.date_select.replace('\n','')))
                #print(len(self.dayslist_inMonth[0]))
                #print(self.date_select)
                #print(self.dayslist_inMonth[0])
                #print(self.dayslist_inMonth[0] == self.date_select)
                self.summary_log.insert(END,'\n---当日无记录！')
                self.summary_log.insert(END,'\n- - - - - - - - - - - - - - - - - - - - - -\n')
                self.dialog = True

        except AttributeError:
            pass

        self.enter_dialog()


    def enter_dialog(self):
        if self.dialog == True:
            if self.Month < 10:
                self.summary_log.insert(END,'\n---请输入需要查阅的日期： {}-0{}-'.format(str(self.Year),str(self.Month)))
            else:
                self.summary_log.insert(END,'\n---请输入需要查阅的日期： {}-{}-'.format(str(self.Year),str(self.Month)))
                #self.summary_log.focus_force()

        else:
            with open('.\\data\\' + file_name + '.txt',"r") as f:
                data = f.read()
                record_list = data.split('\n\n\n\n\n')
                #print(record_list)
            for i in record_list:
                #print(i)
                if self.date_select.replace('\n','') in i:
                    
                    self.summary_log.insert(END,'\n'+ i)
                    self.summary_log.insert(END,'\n- - - - - - - - - - - - - - - - - - - - - -')
            record_list =[]
            if self.Month < 10:
                self.summary_log.insert(END,'\n\n\n---请输入需要查阅的日期： {}-0{}-'.format(str(self.Year),str(self.Month)))
            else:
                self.summary_log.insert(END,'\n---请输入需要查阅的日期： {}-{}-'.format(str(self.Year),str(self.Month)))

    def backup(self):
        global backupdir
        self.summary_log.delete(0.0,END)
        rootdir= '.\\data'
        absdir = path.abspath(path.dirname(rootdir))
        #print(absdir)
        for (dirpath,dirnames,filenames) in walk(rootdir):
            #print(dirpath,dirnames,filenames)
            for filename in filenames:
                if path.splitext(filename)[1] == '.txt':
                    copycmd = 'copy "{}\\data\\{}" "{}\\{}"'.format(absdir,filename,backupdir,filename)
                    print(copycmd)
                    if system(copycmd) == 0:
                        self.summary_log.insert(END,'\n---{} 备份成功！'.format(filename))
                        self.summary_log.insert(END,'\n---备份路径： {}  \n---如需更改备份路径，可以去配置文件上面改'.format(backupdir))
                        self.summary_log.insert(END,'\n\n- - - - - - - - - - - - - - - - - - - - - -')
                    else:
                        self.summary_log.insert(END,'\n---{} 备份失败！'.format(filename))



if __name__=="__main__":
    cmd_index = 0
    user_command = ''
    file_name = ''
    content_first = ''
    root = Tk()
    Application(root)
    root.mainloop()
