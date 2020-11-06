from tkinter import *
import pyautogui as pg
import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


DD = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
DD30 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
        '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
DD31 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
        '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

year1StHalf = ['Jan', 'Feb', 'Mar']
monthOtherY_dict = {'Apr': 487, 'May': 506, 'Jun': 524, 'Jul': 543, 'Aug': 560, 'Sep': 577, 'Oct': 593, 'Nov': 615,
                    'Dec': 631, 'Jan': 649, 'Feb': 667, 'Mar': 685}

month20172018Y_dict = {'Jul': 487, 'Aug': 506, 'Sep': 524, 'Oct': 543, 'Nov': 560, 'Dec': 577, 'Jan': 593, 'Feb': 615,
                       'Mar': 631}
curIdx = 0

mon30 = ['Apr', 'Jun', 'Sep', 'Nov']
mon31 = ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec']
monthOther = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month2017 = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
curYearMonth = [monthOther[_m] for _m in range(datetime.datetime.today().month)]
month_to_num = {'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', 'Jan': '01', 'Feb': '02', 'Mar': '03'}
num_to_month = {int(month_to_num[k]): k for k in month_to_num}

years = [x for x in range(2017, int(datetime.datetime.today().year)+1)]


def startDownloadCC(monthList, CC):
    googleIconX, googleIconY = 514, 747
    reX, reY = 85, 50
    dbX, dbY = 1348, 698
    pleaseWaitImg = 'assets\\Please Wait(Cd).png'

    if CC == 'Cash Ledger':
        fx, fy = 300, 481
        tx, ty = 650, 481
        gox, goy = 907, 481
        saveX, saveY = 964, 549
        noDataImg = 'assets\\No data available img.png'
        downloadSleep = 3.5

    elif CC == 'Credit Ledger':
        fx, fy = 267, 454
        tx, ty = 642, 457
        gox, goy = 904, 452
        saveX, saveY = 951, 536
        noDataImg = 'assets\\No data available (Cd) img.png'
        downloadSleep = 2.5

    sleep(1)
    pg.click(googleIconX, googleIconY)
    sleep(2)

    pg.click(dbX, dbY)
    sleep(0.5)
    pg.click(reX, reY)
    sleep(5)



    isDownloadBarUp = True
    for FMonth, TMonth in monthList:

        pg.click(fx, fy)
        sleep(0.5)
        pg.write(FMonth)
        sleep(1.5)

        pg.click(tx, ty)
        sleep(0.5)
        pg.write(TMonth)
        sleep(1.5)

        pg.click(gox, goy)
        sleep(2)

        isDataAvailable = pg.locateOnScreen(noDataImg)

        if isDataAvailable == None:
            pg.vscroll(-2000)
            sleep(1.5)

            pg.click(saveX, saveY)
            sleep(downloadSleep)

            isPleaseWait = pg.locateOnScreen(pleaseWaitImg)
            while isPleaseWait != None:
                sleep(0.1)
                isPleaseWait = pg.locateOnScreen(pleaseWaitImg)

            pg.vscroll(2000)
            sleep(1.5)

            if isDownloadBarUp:
                saveY -= 50
                # fy += 25
                # ty += 25
                # goy += 25
                isDownloadBarUp = False

        else:
            pg.click(reX, reY)
            sleep(0.8)
            Label(root, text=f'No Data Available for period {FMonth} to {TMonth}').grid()
            sleep(5)
            continue


def monthListFor3B(sd, ed):
    global curIdx

    listOfMonthForWhich3bIsToBeDownloaded = []

    def next(list):
        global curIdx
        try:
            ret = list[curIdx]
            curIdx += 1
            return ret
        except IndexError:
            curIdx = 0
            ret = list[curIdx]
            curIdx += 1
            return ret

    def iterMonthList(year):
        if year == 2017:
            return month2017
        else:
            return monthOther

    sdd, sdm, sdy = sd.split('/')
    edd, edm, edy = ed.split('/')

    if sdy == '2017':
        curIdx = month2017.index(sdm)
    else:
        curIdx = monthOther.index(sdm)

    year_it = int(sdy)
    run = True
    run1 = True
    while run:
        month_it_list = iterMonthList(year_it)

        if run1:
            noOfmonth = 13 - int(month_to_num[sdm])
        else:
            noOfmonth = 12

        for _m in range(noOfmonth):
            month = next(month_it_list)
            my_tirger = str(month + " " + str(year_it))

            if month in year1StHalf:
                my = str(month + " " + str(year_it-1)+"-"+str(year_it))
            else:
                my = str(month + " " + str(year_it)+"-"+str(year_it+1))

            listOfMonthForWhich3bIsToBeDownloaded.append(my)
            if my_tirger == str(edm+" "+edy):
                run = False
                break
        run1 = False
        year_it += 1
        curIdx = 0

    return listOfMonthForWhich3bIsToBeDownloaded


def getMonthDict(y):
    if y == "2017-2018":
        return month20172018Y_dict
    else:
        return monthOtherY_dict


def creOrderedYear_YCoordinet_List():
        curYear = datetime.datetime.today().year
        curMonth = datetime.datetime.today().month

        if curMonth <= 3:
            yearList = [str(x) + "-" + str(x + 1) for x in range(2017, curYear)]
        else:
            yearList = [str(x) + "-" + str(x + 1) for x in range(2017, curYear + 1)]

        lastYear = yearList[-1]
        yearList.remove(yearList[-1])
        finalYearList = []
        idx = -1
        for x in range(0, len(yearList)):
            finalYearList.append(yearList[idx])
            idx -= 1
        finalYearList.append(lastYear)

        yearY_dict = {}
        yCoordinet = 487

        for y in finalYearList:
            yearY_dict[y] = yCoordinet
            yCoordinet += 20

        return yearY_dict


def startDownloadGST3b(sd, ed):
    listOf3BfileDate = monthListFor3B(sd, ed)

    clickSleep = 1.5
    selectionSleep = 2
    scrollSleep = 1.5
    downloadSleep = 3.5

    googleIconX, googleIconY = 514, 747
    reX, reY = 85, 50
    dbX, dbY = 1348, 698

    monthBoxX, monthBoxY = 622, 460
    yearBoxX, yearBoxY = 271, 460
    selectX, selectY = 929, 460
    downloadX, downloadY = 1153, 505

    monthX = 622
    yearX = 271

    sleep(1)
    pg.click(googleIconX, googleIconY)
    sleep(2)

    pg.click(dbX, dbY)
    sleep(0.5)
    pg.click(reX, reY)
    sleep(13)


    run1 = True
    changeFY = False
    for _dt in listOf3BfileDate:
        m, fy = _dt.split(' ')
        monthY_dict = getMonthDict(fy)
        yearY_dict = creOrderedYear_YCoordinet_List()

        if run1:
            #set year
            pg.click(yearBoxX, yearBoxY)
            sleep(clickSleep)
            yearY = yearY_dict[fy]
            pg.click(yearX, yearY)
            sleep(clickSleep)

        if changeFY:
            pg.click(yearBoxX, yearBoxY)
            sleep(clickSleep)
            yearY = yearY_dict[fy]
            pg.click(yearX, yearY)
            sleep(clickSleep)
            changeFY = False

        if m == 'Mar':
            changeFY = True


        monthY = monthY_dict[m]

        pg.click(monthBoxX, monthBoxY)
        sleep(clickSleep)
        pg.click(monthX, monthY)
        sleep(clickSleep)

        pg.click(selectX, selectY)
        sleep(selectionSleep)
        pg.vscroll(-2000)
        sleep(scrollSleep)

        pg.click(downloadX, downloadY)
        sleep(downloadSleep)

        pg.vscroll(2000)
        sleep(scrollSleep)

        if run1:
            downloadY -= 50
            run1 = False


def getStartEndDate():
    global f_DDvar, f_MMvar, f_YYYYvar, t_DDvar, t_MMvar, t_MMvar
    startDate = f_DDvar.get() + '/' + f_MMvar.get() + '/' + f_YYYYvar.get()
    endDate = t_DDvar.get() + '/' + t_MMvar.get() + '/' + t_YYYYvar.get()
    return (startDate, endDate)

def getStartEndMonthlist(sd, ed):
    global month_to_num, num_to_month
    se_month_list = []

    sdd, sdm, sdy = sd.split('/')
    edd, edm, edy = ed.split('/')

    gsd = datetime.date(int(sdy), int(month_to_num[sdm]), int(sdd))
    ged = ''

    nextsd = gsd
    td = datetime.date(int(edy), int(month_to_num[edm]), int(edd)).strftime("%d/%m/%Y")

    while ged != td:

        finalSD = ''
        finalED = ''

        finalSD = nextsd
        tempD = finalSD + relativedelta(months=3)
        if num_to_month[tempD.month] in mon31:
            finalED = datetime.date(tempD.year, tempD.month, 31)
        else:
            finalED = datetime.date(tempD.year, tempD.month, 30)
        nextsd = datetime.date(tempD.year, tempD.month, 1)
        ged = finalED.strftime("%d/%m/%Y")

        finalSD = finalSD.strftime("%d/%m/%Y")
        finalED = finalED.strftime("%d/%m/%Y")
        se_month_list.append((finalSD, finalED))

    return se_month_list


def isLeapyear(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def traceFY(*args):

    traceFM()

def traceFM(*args):
    global f_DD, f_MM, f_MMvar, f_DDvar, f_YYYYvar

    month = f_MMvar.get()
    curDD = f_DDvar.get()
    year = int(f_YYYYvar.get())
    LeapYear = isLeapyear(year)
    row = 0

    f_MM.destroy()
    f_MMvar = StringVar()
    if year == 2017:
        if month not in month2017:
            f_MMvar.set(month2017[-1])
        else:
            f_MMvar.set(month2017[month2017.index(month)])
        f_MM = OptionMenu(date_F, f_MMvar, *month2017)
    elif year == datetime.datetime.today().year:
        if month not in curYearMonth:
            f_MMvar.set(curYearMonth[-1])
        else:
            f_MMvar.set(curYearMonth[curYearMonth.index(month)])
        f_MM = OptionMenu(date_F, f_MMvar, *curYearMonth)
    else:
        if month not in monthOther:
            f_MMvar.set(monthOther[-1])
        else:
            f_MMvar.set(monthOther[monthOther.index(month)])

        f_MM = OptionMenu(date_F, f_MMvar, *monthOther)
    f_MM.grid(padx=padx, pady=pady, column=2, row=row)

    if month in mon30:

        f_DDvar = StringVar()
        if curDD != '31':
            f_DDvar.set(curDD)
        else:
            f_DDvar.set(DD30[-1])

        f_DD.destroy()
        f_DD = OptionMenu(date_F, f_DDvar, *DD30)
        f_DD.grid(padx=5, pady=3, column=1, row=row)

    elif month in mon31:

        f_DDvar = StringVar()
        if curDD != '31':
            f_DDvar.set(curDD)
        else:
            f_DDvar.set(DD31[-1])

        f_DD.destroy()
        f_DD = OptionMenu(date_F, f_DDvar, *DD31)
        f_DD.grid(padx=5, pady=3, column=1, row=row)

    elif month == 'Feb':
        if LeapYear:
            DD28_29 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29']

        else:
            DD28_29 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']


        f_DDvar = StringVar()

        if curDD != '31' or curDD != '30' or curDD == '29':
            f_DDvar.set(curDD)
            if curDD == "29" and not LeapYear:
                f_DDvar.set('28')
        else:
            f_DDvar.set(DD28_29[-1])

        f_DD.destroy()
        f_DD = OptionMenu(date_F, f_DDvar, *DD28_29)
        f_DD.grid(padx=5, pady=3, column=1, row=row)


def traceTY(*args):
    traceTM()

def traceTM(*args):
    global t_DD, t_MM, t_MMvar, t_DDvar, t_YYYYvar

    month = t_MMvar.get()
    curDD = t_DDvar.get()
    year = int(t_YYYYvar.get())
    LeapYear = isLeapyear(year)
    row = 1

    t_MM.destroy()
    t_MMvar = StringVar()
    if year == 2017:
        if month not in month2017:
            t_MMvar.set(month2017[-1])
        else:
            t_MMvar.set(month2017[month2017.index(month)])
        t_MM = OptionMenu(date_F, t_MMvar, *month2017)
    elif year == datetime.datetime.today().year:
        if month not in curYearMonth:
            t_MMvar.set(curYearMonth[-1])
        else:
            t_MMvar.set(curYearMonth[curYearMonth.index(month)])
        t_MM = OptionMenu(date_F, t_MMvar, *curYearMonth)
    else:
        if month not in monthOther:
            t_MMvar.set(monthOther[-1])
        else:
            t_MMvar.set(monthOther[monthOther.index(month)])

        t_MM = OptionMenu(date_F, t_MMvar, *monthOther)
    t_MM.grid(padx=padx, pady=pady, column=2, row=row)

    if month in mon30:

        t_DDvar = StringVar()
        if curDD != '31':
            t_DDvar.set(curDD)
        else:
            t_DDvar.set(DD30[-1])

        t_DD.destroy()
        t_DD = OptionMenu(date_F, t_DDvar, *DD30)
        t_DD.grid(padx=5, pady=3, column=1, row=row)

    elif month in mon31:

        t_DDvar = StringVar()
        if curDD != '31':
            t_DDvar.set(curDD)
        else:
            t_DDvar.set(DD31[-1])

        t_DD.destroy()
        t_DD = OptionMenu(date_F, t_DDvar, *DD31)
        t_DD.grid(padx=5, pady=3, column=1, row=row)

    elif month == 'Feb':
        if LeapYear:
            DD28_29 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29']

        else:
            DD28_29 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']


        t_DDvar = StringVar()

        if curDD != '31' or curDD != '30' or curDD == '29':
            t_DDvar.set(curDD)
            if curDD == "29" and not LeapYear:
                t_DDvar.set('28')
        else:
            t_DDvar.set(DD28_29[-1])

        t_DD.destroy()
        t_DD = OptionMenu(date_F, t_DDvar, *DD28_29)
        t_DD.grid(padx=5, pady=3, column=1, row=row)


def start():
    sd, ed = getStartEndDate()

    if CCRvar.get() == 'Cash Ledger' or CCRvar.get() == 'Credit Ledger':
        FT_Month_list = getStartEndMonthlist(sd, ed)
        startDownloadCC(FT_Month_list, CCRvar.get())

    elif CCRvar.get() == 'GSTR-3B':
        startDownloadGST3b(sd, ed)

if __name__ == '__main__':
    root = Tk()
    root.title('CCR Downloader')
    padx = (5, 5)
    pady = (3, 3)

    date_F = Frame(root)
    date_F.grid(padx=5, pady=3, row=0, column=0)

    row = 0
    f_l = Label(date_F, text="From :")
    f_l.grid(padx=padx, pady=pady, column=0, row=row, sticky=W)

    f_DDvar = StringVar()
    f_DDvar.set(DD[0])

    f_DD = OptionMenu(date_F, f_DDvar, *DD)
    f_DD.grid(padx=padx, pady=pady, column=1, row=row)

    f_MMvar = StringVar()
    f_MMvar.set(month2017[0])
    f_MMvar.trace("w", traceFM)
    f_MM = OptionMenu(date_F, f_MMvar, *month2017)
    f_MM.grid(padx=padx, pady=pady, column=2, row=row)

    f_YYYYvar = StringVar()
    f_YYYYvar.set(years[0])
    f_YYYYvar.trace('w', traceFY)
    f_YYYY = OptionMenu(date_F, f_YYYYvar, *years)
    f_YYYY.grid(padx=padx, pady=pady, column=3, row=row)


    row = 1
    t_l = Label(date_F, text="To :")
    t_l.grid(padx=padx, pady=pady, column=0, row=row, sticky=W)

    t_DDvar = StringVar()
    t_DDvar.set(DD[0])

    t_DD = OptionMenu(date_F, t_DDvar, *DD)
    t_DD.grid(padx=padx, pady=pady, column=1, row=row)

    t_MMvar = StringVar()
    t_MMvar.set(month2017[0])
    t_MMvar.trace("w", traceTM)
    t_MM = OptionMenu(date_F, t_MMvar, *month2017)
    t_MM.grid(padx=padx, pady=pady, column=2, row=row)

    t_YYYYvar = StringVar()
    t_YYYYvar.set(years[0])
    t_YYYYvar.trace('w', traceTY)
    t_YYYY = OptionMenu(date_F, t_YYYYvar, *years)
    t_YYYY.grid(padx=padx, pady=pady, column=3, row=row)

    CCR_list = ['Cash Ledger', 'Credit Ledger', 'GSTR-3B']
    CCRvar = StringVar()
    CCRvar.set(CCR_list[0])
    CCR_OM = OptionMenu(root, CCRvar, *CCR_list)
    CCR_OM.grid(padx=5, pady=3, row=1, column=0)

    start_B = Button(root, text='Start', command=start)
    start_B.grid(padx=5, pady=3, row=2, column=0)
    root.mainloop()

