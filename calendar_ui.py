import calendar 
from tkinter import Tk,Button,Entry,Label,Text,END
# 默认日期
#Year, Month = 2020,3

class Calendar_ui(object):
    def __init__(self,Year,Month):
        self.root = Tk()

        self.root.title(u'日历')
        self.root.geometry('370x280+400+100')
        self.root.minsize(370,280)
        self.root.maxsize(370,280)
        self.Year = Year
        self.Month = Month
        self.ui_update()
        self.button1 = Button(self.root, text='Previous',width =8,height = 1, command=self.ButtonPrevious)
        self.button1.grid(row=len(self.MonthCal)+2, column=1)
        self.button2 = Button(self.root, text='Next',width =8,height = 1, command=self.ButtonNext)
        self.button2.grid(row=len(self.MonthCal)+2, column=5)

    def ui_update(self):
        #print(self.Year)
        #print(self.Month)
        # 首行放置“年、月”的位置
        label = Label(self.root,text=str(self.Year)+"年")
        label.grid(row=0,column=2)
        label = Label(self.root,text=str(self.Month)+"月")
        label.grid(row=0,column=4)
        # labels列表：放置“星期”的标题
        # 用calendar库计算日历
        #global MonthCal
        labels = [['Mon','Tue','Wed','Thu','Fri','Sat','Sun']]
        self.MonthCal = calendar.monthcalendar(self.Year, self.Month)
        #print(MonthCal)
        # 先把界面清空
        for r in range(7):
            for c in range(7):            
                label = Label(self.root,
                              width =5,
                              padx=5,
                              pady=5,
                              text=' ')        
                label.grid(row=r+1,column=c)
        # 把日历加到labels列表中     
        for i in range(len(self.MonthCal)):
            labels.append(self.MonthCal[i])
        #print(self.labels)
        # 放置日历
        for r in range(len(self.MonthCal)+1):
            for c in range(7):
                if labels[r][c] == 0:
                    labels[r][c] = ' '
                label = Label(self.root,
                              width =5,
                              padx=5,
                              pady=5,
                              text=str(labels[r][c]))        
                label.grid(row=r+1,column=c) # 网格布局
        

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

    def run(self):
        self.root.mainloop()

if __name__=="__main__":
    ui_show = Calendar_ui(2020,3)
    ui_show.run()
