import os, time, string, random, tkinter, qrcode
from pystrich.ean13 import EAN13Encoder
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *
from string import digits




#TODO:初始化数据
number = '1234567890'
letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
allis = '1234567890BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+'
i = 0
randstr = []    #记录所有生成的防伪码
fourth = []
fifth = []
randfir = ''    #保存单挑防伪码
randsec = ''
randthr = ''
str_one = ''
strone = ''
strtwo = ''
nextcard = ''
userput = ''
nres_letter = ''



def main_menu():
    print('*'*50)
    print(' '*15+'企业编码生成系统')
    print('*'*50)
    print(' '*3+'1.生成6位数字防伪编码（213563型）')
    print(' '*3+'2.生成9位系列产品数字防伪编码（879-335439型）')
    print(' '*3+'3.生成25位系列产品序列号（B2R12-N7TE8-9IET2-FE35O-DW2K4型）')
    print(' '*3+'4.生成含数据分析功能的防伪编码（5A61M0583D2）')
    print(' '*3+'5.智能批量生成带数据分析的防伪编码')
    print(' '*3+'6.后续补加生成防伪编码')
    print(' '*3+'7.EAN-13条形码批量生成')
    print(' '*3+'8.二维码生成')
    print(' '*3+'9.企业粉丝防伪码抽奖')
    print(' '*3+'0.退出系统')
    print('='*50)
    print(' '*5+'说明：通过数字键选择菜单')
    print('='*50)

    #TODO:  选择
    while True:
        choice = input('请输入您要操作的菜单选项：')
        try:
            choice = int(choice)    #除去英文和浮点数还有符号
        except:
            print('\033[1;31;40m输入非法错误，请重新输入！！\033[0m')
            time.sleep(2)
            continue
        else:
            
            if choice == 0:
                print('\033[1;33m     正在退出系统！\033[0m')
                time.sleep(0.5)
                exit()
                
            elif choice == 1:
                scode1(str(choice))     #生成防伪码
                
            elif choice == 2:
                scode2(choice)
                
            elif choice == 3:
                scode3(choice)

            elif choice == 4:
                scode4(choice)

            elif choice == 5:
                scode5(choice)

            elif choice == 6:
                scode6(choice)

            elif choice == 7:
                scode7(choice)

            elif choice == 8:
                scode8(choice)
            
            elif choice == 9:
                scode9(choice)
            
            else:
                continue
                    

def mkdir(path):
    '''创建文件夹'''
    i = os.path.exists(path)    #判断是否存在该文件夹
    if not i:                   #若不存在则新建该文件夹
        os.mkdir(path)


def openfile(filename):
    '''读取文件'''
    with open(filename) as file:
        data = file.read()
    return data


def inputbox(showstr, showorder, length):
    '''输入验证判断'''
    instr = input(showstr)  #输入提示
        #分成三种验证：
        #   1.数字，不限长度
        #   2.字母，长度有限制
        #   3.数字，长度有限制

    #TODO: 验证第一种
    if showorder == 1:
        #要求输入大于0的整数
        try:
            num = int(instr)    #把输入的类型转化为int类型
        except:                 #这一步排除了str和flost类型
            print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
            return '0'
        else:
            if num <= 0:    #排除不大于0的情况
                print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
                return '0'
            else:
                return num


    #TODO:  验证第二种
    if showorder == 2:
        #排除长度不符的输入
        if len(instr) != length:
            print('     \033[1;31;40m输入有误，请重新输入！！\033[0m')
            return '0'
        
        #需要循环检查是否全是字母
        for i in range(length):
            if str.isdigit(instr[i]):   #发现是数字报错警告
                print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
                return '0'
            if ord(instr[i])<65 or ord(instr[i])>122 or 90<ord(instr[i])<97:  #65-90 97-122
                print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
                return '0'
        return instr
    
    #TODO:  验证第三种
    if showorder == 3:
        
        #和第一种差不多，但是长度有限制,000-099这里可以，第一种不行
        if len(instr)<3:
            print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
            return '0'
        try:
            num = int(instr)    #把输入的类型转化为int类型
        except:                 #这一步排除了str和flost类型
            print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
            return '0'
        else:
            if num > 10**length-1 or num < 0:     #排除长度过长的,3位（000-099）
                print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
                return '0'
            else:
                return str(num).zfill(3)
    else:
        print('     \033[1;31;40m输入非法错误，请重新输入！！\033[0m')
        return '0'


def wfile(sstr, save_document, save_file, tips, is_tip=True):
    '''编码输出显示'''
    
    mkdir(save_document)


    save_file = save_file+'-' + str(len(os.listdir(save_document))+1) + '.txt'   #根据文档中文件数量给储存文件命名
    while  os.path.exists(save_document+'/'+save_file):     #防止同名覆盖
        save_file = save_file[:-4] + 'k.txt'
    
    save_path = save_document + '/' + save_file

    with open(save_path, 'w') as f:  #把所有防伪码写入指定的txt文件中
        for i in sstr:
            f.write(i+'\n')
    
    #TODO: 输出提示框
    if is_tip:
        TIPS = tips+': '+str(len(sstr)-1)+'\n防伪码文件存放位置: '+os.getcwd()+'/'+save_path
        tkinter.messagebox.showinfo('提示', TIPS)
    

def scode1(schoice):
    #调用inputbox函数对输入数据进行非空，合法性判断
    snum = inputbox('\033[1;32m     请输入您要生成防伪码的数量：\033[0m', 1, 0)
    
    while snum == '0':      #防止错误输入
        snum = inputbox('\033[1;32m     请输入您要生成防伪码的数量：\033[0m', 1, 0)
    
    randstr.clear()     #清空保存防伪码信息
    
    for i in range(int(snum)+1):
        randfir = ''        #设置存储单条防伪码变量为空
        if i == 0:
            randfir = '1'+',---,'+str(snum)
        else:
            for j in range(6):
                randfir += random.choice(number)    #随机生成6个数字作为防伪码
        randstr.append(randfir)     #把生成好的防伪码放入list保存中
    




    save_document = 'codepath' 
    save_file = 'scode1'
    wfile(randstr, save_document, save_file, '已生成6位防伪码共计')
    print('     \033[1;34;47m已经执行完毕！！！\033[0m')


def scode2(schoice):
    #调用inputbox函数对输入数据进行非空，合法性判断
    is_ok = inputbox('\033[1;32m     请输入系列产品的数字起始号(3位)：\033[0m', 
    3, 3)   #该防伪码全面3个数字用户输入，后面6个数字随机生成

    while  is_ok == '0':
        is_ok = inputbox('\033[1;32m     请输入系列产品的数字起始号(3位)：\033[0m', 
    3, 3)

    randstr.clear()     #清空保存防伪码信息
    snum = input('\033[1;32m     请输入生成数量：\033[0m')      #输入生成数量
    while snum == '0':
        snum = input('\033[1;32m     请输入生成数量：\033[0m')      #输入生成数量
    for i in range(int(snum)+1):
        randfir = is_ok     #把防伪码前三位赋值给randfir
        if i == 0:
            randfir = '2,'+is_ok+','+str(snum)
        else:
            for j in range(6):
                randfir += random.choice(number)    #随机生成防伪码后六位
        randstr.append(randfir)     #把生成好的防伪码放入randstr
    
    save_document = 'codepath'
    save_file = 'scode2'

    wfile(randstr, save_document, save_file, '已生成9位系列产品防伪码共计')
    print('     \033[1;34;47m已经执行完毕！！！\033[0m')


def scode3(schoice):
    '''内容和1差不多'''
    #输入要生成防伪码的数量
    snum = inputbox('\033[1;32m     请输入要生成的25位混合产品系列防伪码的数量：\033[0m', 1, 0)

    while snum == '0':
        snum = inputbox('\033[1;32m     请输入要生成的25位混合产品系列防伪码的数量：\033[0m', 1, 0)

    randstr.clear()     #清空列表

    for i in range(int(snum)+1):  
        strone = ''
        if i == 0:
            strtwo = '3'+',---,'+str(snum)
        else:
            for j in range(25):
                strone  += random.choice(letter)
            strtwo = strone[:5]+'-'+strone[5:10]+'-'+strone[10:15]+'-'+strone[20:25]
        randstr.append(strtwo)

    save_document = 'codepath' 
    save_file = 'scode3'
    

    wfile(randstr, save_document, save_file, '已生成25位混合产品系列防伪码共计：')
    print('     \033[1;34;47m已经执行完毕！！！\033[0m')



def scode4(schoice):
    '''生成含数据分析功能的防伪编码'''
        
    is_ok = inputbox('\033[1;32m     请输入数据分析编号(3位字母)：\033[0m', 
    2, 3)   #用户随机输入三个字母用于数据分析

    while is_ok == '0':
        is_ok = inputbox('\033[1;32m     请输入数据分析编号(3位字母)：\033[0m', 
    2, 3) 


    snum = inputbox('\033[1;32m     请输入要生成的带数据分析功能的防伪码数量：\033[0m', 
    1, 0)
    
    while snum == '0':
        snum = inputbox('\330[1;32m     请输入要生成的带数据分析功能的防伪码数量：\330[0m', 
    1, 0)
    ffcode(is_ok, snum)
    wfile(randstr, 'codepath', 'scode4', '生成含数据分析功能的防伪码共计：')
    print('     \033[1;34;47m已经执行完毕！！！\033[0m')

def ffcode(is_ok, snum):
    randstr.clear()
    is_ok = is_ok.upper()
    for i in range(int(snum)+1):
        randfir = ''
        if i == 0:
            randfir = '4,'+is_ok+','+str(snum)
        else:
            loc = sorted(random.sample(range(9), 3))
            for j in range(9):
                if j == loc[0]:
                    randfir += is_ok[0]
                elif j == loc[1]:
                    randfir += is_ok[1]
                elif j == loc[2]:
                    randfir += is_ok[2]
                else:
                    randfir += random.choice(number)
    
        randstr.append(randfir)

         
def scode5(schoice):
    default_dir = r'autocode.mri'    #设置默认打开的文件夹
    
    #打开文件夹选择对话框，指定打开的文件夹称为‘codeauto.aut’，扩展名位’.mri‘
    #可以使用记事本打开和编辑

    file_path = tkinter.filedialog.askopenfilename(
        filetypes=[('Text file', '*.mri')], 
        title=u'请选择只能批量处理文件', 
        initialdir=(os.path.expanduser(default_dir)))
    try:
        codelist = openfile(file_path)      #读取从文件选择对话框中选中的文件
        
    except:
        for i in range(3):
            print('     \033[1;31;40m你没有选择文件,正在退回到菜单！！\033[0m')
        time.sleep(0.3)
        main_menu()
    
    else:
        codelist = codelist.split('\n')#以换行符为分隔读取的信息内容转换为列表
        print(codelist)
        for item in codelist:   #按读取的信息循环生成防伪码
            codea, codeb = item.split(',')[0], item.split(',')[1]
            ffcode(codea, codeb)
            wfile(randstr, 'codepath', 'scode5', '生成含数据分析功能的防伪码共计：')
    print('     \033[1;34;47m已经执行完毕！！！\033[0m')


def scode6(schoice):
    default_dir = r'codepath'   #默认打开文件

    file_path = tkinter.filedialog.askopenfilename(
        filetypes=[('Text file', '*.txt')], 
        title=u'请选择已经生成的防伪码文件', 
        initialdir=(os.path.expanduser(default_dir)))

    try:
        codelist = openfile(file_path)
        
    except:
        for i in range(3):
            print('     \033[1;31;40m你没有选择文件,正在退回到菜单！！\033[0m')
        time.sleep(0.3)
        main_menu()
    else:
        try:
            codelist = codelist.split('\n')
            codelist.remove('')     #删除最后一个空行
            strset = codelist[0].split(',')    #取出一行用于查看该防伪码的规律
            num = strset[2]
            if strset[0] == '1':
                
                addlist, addlen = askyesno('',int(num),1)
                newnum = int(num) + int(addlen)
                codelist[0] = codelist[0][:-len(num)] + str(newnum)
                codelist = codelist+addlist
                with open(file_path, 'w') as f:
                    for i in codelist:
                        f.write(i+'\n')

            elif strset[0] == '2':
                addlist, addlen = askyesno(strset[1],int(num),2)
                newnum = int(num) + int(addlen)
                codelist[0] = codelist[0][:-len(num)] + str(newnum)
                codelist = codelist+addlist
                with open(file_path, 'w') as f:
                    for i in codelist:
                        f.write(i+'\n')
            elif strset[0] == '3':
                addlist, addlen = askyesno('',int(num),3)
                newnum = int(num) + int(addlen)
                codelist[0] = codelist[0][:-len(num)] + str(newnum)
                codelist = codelist+addlist
                with open(file_path, 'w') as f:
                    for i in codelist:
                        f.write(i+'\n')
            elif strset[0] == '4':
                addlist, addlen = askyesno(strset[1],int(num), 4)
                newnum = int(num) + int(addlen)
                codelist[0] = codelist[0][:-len(num)] + str(newnum)
                codelist = codelist + addlist
                with open(file_path, 'w') as f:
                    for i in codelist:
                        f.write(i+'\n')
        except:
            for i in range(3):
                print('     \033[1;31;40m你没有正确选择文件,正在退回到菜单！！\033[0m')
            time.sleep(0.3)
            main_menu()
            
        
def askyesno(info, num, choice):
    var_box = tkinter.messagebox.askyesno(title='系统提示',message='之前防伪码共计：'+str(num)+'\n是否需要补充防伪码')#返回'True','False'

    if var_box:
        snum = inputbox('请输入要补充的防伪码数量：', 1, 0)
        while snum == '0':
            snum = inputbox('请输入要补充的防伪码数量：', 1, 0)
        randstr.clear()
        for i in range(int(snum)):
            if choice == 1 or choice==2:
                randfir=info
                for j in range(6):
                    randfir += random.choice(number)
                randstr.append(randfir)
            elif choice == 3:
                strone=info
                for j in range(25):
                    strone  += random.choice(letter)
                strtwo = strone[:5]+'-'+strone[5:10]+'-'+strone[10:15]+'-'+strone[20:25]
                randstr.append(strtwo)
            elif choice == 4:
                randstr.clear()
                for i in range(int(snum)):
                    randfir=''
                    loc = sorted(random.sample(range(9), 3))
                    for j in range(9):
                        if j == loc[0]:
                            randfir += info[0]
                        elif j == loc[1]:
                            randfir += info[1]
                        elif j == loc[2]:
                            randfir += info[2]
                        else:
                            randfir += random.choice(number)
                    randstr.append(randfir)

        return randstr, snum  
    else:
        print('不作处理！')


def scode7(schoice):
    mainid = inputbox('\033[1;32m       请输入EN13的国家代码（3位）：\033[0m', 3, 3)
    while mainid == '0':
        mainid = inputbox('\033[1;32m       请输入EN13的国家代码（3位）：\033[0m', 3, 3)
    
    compid = inputbox('\033[1;32m       请输入企业代码（4位）：\033[0m', 3, 4)
    while compid == '0':
        compid = inputbox('\033[1;32m       请输入企业代码（4位）：\033[0m', 3, 4)
    
    incount = inputbox('\033[1;32m      请输入要生成的条形码数量：\033[0m', 1, 0)
    while incount == '0':
        incount = inputbox('\033[1;32m      请输入要生成的条形码数量：\033[0m', 1, 0)

    mkdir('barcode')    #该文件夹保存条形码文件
    
    for i in range(int(incount)):   #批量生成条形码
        strone = mainid+compid  #这里是3+4=7位，随机生成5位，通过计算生成最后一位校验码
        for i in range(5):
            strone += random.choice(number)
        #TODO:  计算最后一位校验码
        evensum = int(strone[1])+int(strone[3])+int(strone[5])+int(strone[7])+int(strone[9])+int(strone[11])
        oddsum = int(strone[0])+int(strone[2])+int(strone[4])+int(strone[6])+int(strone[8])+int(strone[10])
        checkbit = (10-(evensum*3+oddsum)%10)%10
        barcode = strone + str(checkbit)    #获得13位条形码
        encode = EAN13Encoder(barcode)      #生成条形码图片
        encode.save('barcode/'+barcode+'.png')       #设置保存路径
    print('\033[1;32m      已经生成%s个条形码！！\033[0m'%incount)



def scode8(schoice):
    Text = input('\033[1;32m       请输入二维码内容：\033[0m')
    name = input('\033[1;32m       生成二维码名字：\033[0m')
    qr = qrcode.make(Text)
    qr.save('qrcode/'+name+'.png')
    print('\033[1;32m       成功生成二维码！\033[0m')



def scode9(schoice):
    default_dir = r'codepath'   #默认打开文件

    file_path = tkinter.filedialog.askopenfilename(
        filetypes=[('Text file', '*.txt')], 
        title=u'请选择抽奖名单文件：', 
        initialdir=(os.path.expanduser(default_dir)))

    try:
        codelist = openfile(file_path)  #打开抽奖文件
        codelist = codelist.split('\n') #分割信息
        incount = inputbox('\033[1;32m      请输入中奖的个数：\033[0m', 1, 0)
        while int(incount)==0 or int(codelist[0].split(',')[-1])<int(incount):
            incount = inputbox('\033[1;32m      请输入中奖的个数：\033[0m', 1, 0)
        
        strone = random.sample(codelist[1:], int(incount))
        print('\033[1;32m      一下是中奖名单：\033[0m')
        for i in range(int(incount)):

            print("\033[1;36m %s\033[0m"%strone[i])

    except:
        for i in range(3):
            print('     \033[1;31;40m你没有正确选择文件,正在退回到菜单！！\033[0m')
        time.sleep(0.3)
        main_menu()
