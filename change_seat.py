"""
작성자: 임재욱
버전:ver.3
마지막 수정일자: 2023/07/18
작성목적: 트러블 슈팅
"""


from tkinter import *
from functools import partial
import random as rand       #난수생성 모듈
import math                 #수학관련 계산 모듈    
import time as t            #시간 지연등 시간 관련 모듈
import os                   #파일 경로 탐색에 사용



stu_num=0
desk_num=0
stu_ept=" "



#함수선언

#파일을 체크하고 빈 파일이면 삭제하는 함수(x)
def check_del(f_data,f_path):
    if(f_data.readline()==''):
        f_data.close(6)           #안 닫고 삭제하려 하면 오류
        os.remove(f_path)
    else:
        f_data.close()
def notice(message):
    warn=Tk()
    warn.title("notice")
    warn.geometry("400x200")
    warn.configure(bg='#12fb0c')
    warn.option_add("*Font","궁서 15")
    lab1=Label(warn,text=message,width='40',height='12')
    lab1.pack()
    warn.mainloop()
#학생수 조건 체크 함수(x)
def stu_check(stu_num):
    flag=-1
    if stu_num.isdigit()==0 or int(stu_num)==0:         #학생수가 문자,소수,음수,0이라면 continue해서 다시 학생수 입력
        #print("마지막 학생의 번호는 자연수 입니다. 다시 입력해주세요.")
        flag=1
    elif int(stu_num)>=100:                             #일단 문자가 걸리지므로 int()로 정수 변환 가능, 100명 이상이면 continue해서 마지막 학생의 번호 다시 입력
        #print("마지막 학생의 번호는 100미만의 자연수입니다. 다시 입력해주세요.")
        flag=1
    if flag==1:
        notice("마지막 학생의 번호는 100미만의 자연수입니다. \n다시 입력해주세요.")
        return False
    return True

#책상의 가로 개수 조건 체크 함수(x)
def desk_check(desk,stu):
    flag=-1
    if desk.isdigit()==0 or int(desk)==0:               #학생수가 문자,소수,음수,0이라면 continue해서 다시 책상 가로 수 입력
        #print("책상의 가로 개수는 자연수입니다. 다시 입력해주세요.")  
        flag=1
    elif(int(stu)<int(desk)):                   #(학생수)<(책상 가로 수)일 필요도 없고 이상해서 continue해서 다시 책상 가로 수 입력, 걸러져서 int()로 변환 가능,
        #print("책상의 가로 개수는 마지막 학생의 번호보다 클 수 없습니다. 다시입력해주세요")
        flag=2
    if flag==1:
        notice("책상 열의 개수는 자연수입니다. \n다시 입력해주세요.")
        return False
    elif flag==2:
        notice("책상 열의 개수는 마지막 학생의 번호보다 클 수 없습니다. \n다시 입력해주세요.")
        return False
    return True

#자리 랜덤 배치 함수(x)
def rand_arr(stu_num,desk_num):
    desk_list=[[None for col in range(desk_num)]for row in range(math.ceil(stu_num/desk_num))]      #desk_list라는 이차원 리스트 생성((책상가로수)*((학생수)/(책상 가로 수)를 올림한 값)),range는 0부터 설정값-1까지 
    stu_list=[False for col in range(stu_num+1)]        #학생수+1개의 원소를 갖는 리스트를 생성 및 False로 초기화, 편이를 위해 0은 사용하지 않음

    cnt=0                                               #cnt=count를 0으로 초기화
    flag=0                                              #flag를 0으로 초기화
            
    for i in range(math.ceil(stu_num/desk_num)):        #i반복
        for j in range(desk_num):                       #j반복
            while True:                                 #무한반복(2-2)
                rand_num=rand.randrange(1,stu_num+1)    #1~학생수까지 정수 중에 난수 생성
                if stu_list[rand_num]==False:           #난수 번호가 전에 추첨되지 않은 경우, 이미 추첨되면 다시 무한반복2-2로 돌아감
                    desk_list[i][j]=rand_num            #현재 책상에 해당 번호 넣음
                    stu_list[rand_num]=True             #해당 학생 번호를 True로 바꿈
                    break                               #2-2무한반복 탈출
            cnt+=1                                      #cnt를 1 올림(추첨된 책상 수 카운트)
            if cnt>=stu_num:                            #추첨된 책상수>=학생수이면 flag=1,j반복 탈출
                flag=1
                break
        if flag==1:                                     #flag=1이면 i반복 탈출
            break
        
    return desk_list

#배열(배치) 출력 함수(x)
def arr_print(stu_num,desk_num,desk_list):
    flag=0
    cnt=0
    for i in range(math.ceil(stu_num/desk_num)):        #i반복
        for j in range(desk_num):                       #j반복
            print(desk_list[i][j],end="")               #desk_list[i][j]출력
            for k in range(5-len(str(desk_list[i][j]))):        #줄맞추기용 k반복, 5-숫자 자리 수 만큼 띄움
                print(" ",end="")                       #띄어쓰기                                              

            cnt+=1                                      #cnt를 1만큼 더함(출력된 책상 수 카운트)
            if cnt>=stu_num:                            #출력된 책상수 >= 학생수 면 flag=1,j반복 탈출
                flag=1              
                break
        print()    
        if flag==1:                                     #flag가 1이면 i반복 탈출
            print("성공적으로 추첨되었습니다.")
            break
    return True

#배열(배치) 저장 여부 확인 및 저장 함수(x) 
def arr_save(stu_num,desk_num,desk_list):
    flag=0                                                  #flag를 0으로 초기화
    cnt=0                                                   #cnt를 0으로 초기화
    while True:                                             #무한반복(2-3)
        select=input("추첨결과를 저장하시겠습니까?(Y/N)")        #저장여부 확인(일부러 소문자 허용 안함)
        if select=='Y':                                     #첫 대답 Y이면
            while True:                                     #무한반복(2-4)
                re_select=input("정말로 추첨결과를 저장하시겠습니까?(Y/N)")     #저장여부 재확인(전 데이터가 날라가기 때문에)
                if re_select=='Y':                          #두번째 대답 Y이면(자리 배치 출력과 유사)
                    f_seat=open("seat.txt",'w')             #seat.txt를 write 모드로 오픈
                    for i in range(math.ceil(stu_num/desk_num)):        #i반복
                        for j in range(desk_num):                       #j반복
                            f_seat.write(str(desk_list[i][j]))          #seat.txt에 desk_list[i][j]를 입력
                            for k in range(5-len(str(desk_list[i][j]))):        #k반복, 다시 출력할 때 그대로 출력할거라서 줄 맞추기
                                f_seat.write(" ")           #" "을 seat.txt에 입력
                            cnt+=1                          #여기서도 마찬가지로 카운트
                            if cnt>=stu_num:                #여기서도 카운트 >= 학생수 면
                                flag=1                      #또 flag=1
                                break                       #j반복 탈출
                        f_seat.write('\n')                  #\n을 seat.txt에 입력
                        if flag==1:                         #flag=1이면 i반복 탈출
                            break
                    if flag==1:                             #seat.txt를 닫고 무한반복(2-4) 탈출
                        print("성공적으로 추첨결과를 저장했습니다.")
                        f_seat.close()
                        break
                elif re_select=='N':                        #두번쨰 대답이 N이면
                    print("추첨결과를 저장하지 않습니다.")
                    flag=1                                  #flag=1
                    break                                   #무한반복(2-4) 탈출
                else:                                       #두번째 대답 이상 있음,무한반복(2-4) 처음으로
                    print("Y나N을 입력해주세요.")
        elif select=='N':                                   #첫번째 대답 N, 무한반복(2-3)탈출
            print("추첨결과를 저장하지 않습니다.")
            break
        else:                                               #첫번째 대답 이상 있음, 무한반복(2-3)탈출 처음으로
            print("Y나N을 입력해주세요.")
        if flag==1:                                         #flag=1이면 무한반복(2-3) 탈출
            break
        
#파일 초기 설정 함수 
def setting(ran_path,seat_path,name_path):
    flag=0
    ran_exist=os.path.isfile(ran_path)      #range.txt가 있는지 여부 확인, 있으면 True, 없으면 False
    seat_exist=os.path.isfile(seat_path)    #seat.txt가 있는지 여부 확인, 있으면 True, 없으면 False
    name_exist=os.path.isfile(name_path)
    if(ran_exist==True):                    #range.txt가 있으면
        f_ran=open("range.txt",'r')         #range.txt를 read모드로 오픈
        stu_num=f_ran.readline().strip("\n")            #readline()은 \n이 있을때까지 읽어옴,stu_num을 읽어옴
        desk_num=f_ran.readline().strip("\n")           #desk_num을 읽어옴
        stu_ept=f_ran.readline().strip("\n") 
        f_ran.close()                       #range.txt를 닫음(오픈하면 닫아줘야함. 바늘가는데 실간다)
        return stu_num+' '+desk_num+' '+stu_ept
    elif(ran_exist==False):                 #range.txt가 없으면
        flag=1
        f_ran=open("range.txt",'w')         #range.txt를 write모드로 오픈, 없으니 파일이 생성됨.
        f_ran.close()                       #range.txt를 닫음
    if(seat_exist==False):                  #seat.txt가 없다면
        f_seat=open("seat.txt",'w')         #seat.txt를 write모드로 오픈, 없으니 파일이 생성됨
        f_seat.close()                      #seat.txt를 닫음
    if(name_exist==False):
        flag=1
        f_name=open("name.txt",'w')         #range.txt를 write모드로 오픈, 없으니 파일이 생성됨.
        f_name.close() 
    if flag==1:
        return False










#new










def destroy(root):
    root.destroy()
   
def home(cur_path):
    def DnC():
        cur_path.destroy()
        fir_sel()
    btn=Button(cur_path,text="Home",command=DnC,width='5',height='1')
    btn.pack(anchor='nw')



def fir_sel():
    #main창 생성
    main=Tk()
    main.title("Random_Seat")
    main.geometry("1000x600")
    main.configure(bg='#12fb0c')
    main.option_add("*Font","궁서 30")
    #Plab=Label(main)                                                       
    #img=PhotoImage(file="KakaoTalk_20221109_141138894.jpg",master=main)        #적용하려 했던 사진
    #Plab.config(image=img)
    #Plab.pack()
    lab=Label(main,text="자리 랜덤 배치 프로그램",width='20',height='3')      #lab레이블 생성
    lab.pack(pady=30)               #lab레이블 배치
    #선택지
    #1: 기본 정보 입력
    btn1=Button(main)
    btn1.config(text='기본 정보 입력')
    btn1.config(command=lambda:[std_inf(main)])
    btn1.pack(pady=30)
    

    #2: 자리 추첨
    btn2=Button(main)
    btn2.config(text='자리 추첨')
    btn2.config(command=lambda:[rand_seat(main)])
    btn2.pack(pady=30)
    main.mainloop()

    
#기본 정보 입력
def std_inf(main):
    global stu_num,stu_ept,desk_num
    destroy(main)
    sel1=Tk()
    sel1.title("Standard_Information")
    sel1.geometry("1000x600")
    sel1.configure(bg='#12fb0c')
    sel1.option_add("*Font","궁서 30")

    home(sel1)

    lab=Label(sel1,text="기본 정보 입력",width='20',height='3')
    lab.pack(pady=(10,30))
        
    #선택지
    #1: 마지막 학생의 번호, 책상 열의 개수
    btn1=Button(sel1)
    btn1.config(text='마지막 학생의 번호, 제외 번호. 책상 열의 개수')
    btn1.config(command=lambda:[stu_desk(sel1)])
    btn1.pack(pady=30)
    

    #2: 이름 입력
    btn2=Button(sel1)
    btn2.config(text='번호 별 이름')
    btn2.config(command=lambda:[Fname(sel1)])
    btn2.pack(pady=30)
    sel1.mainloop()


def stu_desk(sel1):
    global stu_num,stu_ept,desk_num
    destroy(sel1)
    sel1_1=Tk()
    sel1_1.title("Stu_Desk")
    sel1_1.geometry("1000x600")
    sel1_1.configure(bg='#12fb0c')
    sel1_1.option_add("*Font","궁서 25")

    home(sel1_1)

    lab1=Label(sel1_1,text="마지막 학생의 번호",width='20')
    lab1.pack()
    ent1=Entry(sel1_1)
    ent1.insert(0,stu_num)
    ent1.pack(pady=(15,40))

    lab3=Label(sel1_1,text="제외번호(','로 구분)",width='20')
    lab3.pack(pady=(50,0))
    ent3=Entry(sel1_1)
    ent3.insert(0,stu_ept)
    ent3.pack(pady=(15,40))

    lab2=Label(sel1_1,text="책상 열의 개수(개)",width='20')                                            
    lab2.pack(pady=(40,0))
    ent2=Entry(sel1_1)
    ent2.insert(0,desk_num)
    ent2.pack(pady=(15,0))


    def sd_get_save():
        global stu_num,stu_ept,desk_num
        stu_num=ent1.get()
        desk_num=ent2.get()
        stu_ept=ent3.get()
        #print(desk_num,stu_num)
        if stu_check(stu_num)==True and desk_check(desk_num,stu_num)==True:
            f_ran=open("range.txt",'w')                     
            f_ran.write(stu_num+'\n'+desk_num+'\n'+stu_ept)              
            f_ran.close()
            suc=Tk()
            suc.title("success")
            suc.geometry("300x100")
            suc.configure(bg='#12fb0c')
            suc.option_add("*Font","궁서 15")
            lab1=Label(suc,text="성공적으로 저장했습니다.",width='40',height='12')
            lab1.pack()
            suc.mainloop()
    btn1=Button(sel1_1)
    btn1.config(text="저장")
    btn1.config(command=sd_get_save)
    btn1.pack(pady=30)
    sel1_1.mainloop()


#번호 별 이름 입력
def Fname(sel1):
    destroy(sel1)
    global stu_num, stu_desk 
    global stu_ept
    #str(stu_ept)
    sel1_2=Tk()
    sel1_2.title("Name")
    sel1_2.geometry("1000x600")
    sel1_2.configure(bg='#12fb0c')
    sel1_2.option_add("*Font","궁서 20")
    home(sel1_2)

    stu_num=int(stu_num)
    lab=[0 for i in range(5)]
    ent=[0 for i in range(5)]
    ept=[]
    #print(stu_ept)
    ept=stu_ept.split(",")
    
    
    
    

    
    class myClass:
        cur=1
        end=-1
        cur_ept=[ ]
        global stu_num
        name=[None for i in range(stu_num+1)]           
        f_name=open("name.txt",'r') 
        for i in range(1,stu_num+1):          
            name[i]=f_name.readline().strip("\n")
        f_name.close()

        
        
        def store():
            if myClass.end>0:
                for i in range(myClass.end):
                    myClass.name[i+myClass.cur]=ent[i].get()
            else:  
                for i in range(5):
                    myClass.name[i+myClass.cur]=ent[i].get()
            
        def next():
            if(myClass.cur+4>=stu_num):
                notice("마지막 페이지입니다.")
            
            else:
                myClass.store()
                if len(myClass.cur_ept)>0:
                    for i in range(len(myClass.cur_ept)):
                        lab[int(myClass.cur_ept[i])].configure(state='normal',bg='SystemButtonFace')
                        ent[int(myClass.cur_ept[i])].configure(state='normal',bg='SystemButtonFace')
                    myClass.cur_ept.clear()
                myClass.cur+=5
                cur=myClass.cur
                if myClass.cur+4>=stu_num:
                    s_btn.pack(anchor='se')
                for i in range(5):
                    if stu_num<cur+i:
                        myClass.end=i
                        for j in range(i,5):
                            lab[j].configure(state='disabled',bg='#12fb0c',text="")
                            ent[j].delete(0,len(myClass.name[cur-5+j]))
                            ent[j].configure(state='disabled')
                        break
                    else:
                        lab[i].configure(text=str(cur+i)+"번")
                        ent[i].delete(0,len(myClass.name[cur-5+i]))
                        ent[i].insert(0,myClass.name[cur+i])
                myClass.Fexcept()


        def bef():
            if(myClass.cur-4<=0):
                notice("첫 번째 페이지입니다.")
            else:
                myClass.store()
                if len(myClass.cur_ept)>0:
                    for i in range(len(myClass.cur_ept)):
                        lab[int(myClass.cur_ept[i])].configure(state='normal')
                        ent[int(myClass.cur_ept[i])].configure(state='normal')
                    myClass.cur_ept.clear()
                if myClass.end>0:
                    end=myClass.end
                    for j in range(end,5):
                        lab[j].configure(state='normal',bg='SystemButtonFace')
                        ent[j].configure(state='normal',bg='SystemButtonFace')
                    myClass.end=-1
                else:
                    end=5
                if myClass.cur+5>=stu_num:
                    s_btn.pack_forget()
                myClass.cur-=5
                cur=myClass.cur
                for i in range(end):
                    ent[i].delete(0,len(myClass.name[cur+5+i]))
                for i in range(5):
                    lab[i].configure(text=str(cur+i)+"번")
                    ent[i].insert(0,myClass.name[cur+i])
                myClass.Fexcept()
            
        
            
        def save():
                myClass.store()
                #저장버튼을 마지막에만 두고 중간중간에는 store만    
                f_name=open("name.txt",'w')
                for i in range(1,stu_num+1):
                    f_name.write(myClass.name[i]+'\n')
                f_name.close()
                suc=Tk()
                suc.title("success")
                suc.geometry("300x100")
                suc.configure(bg='#12fb0c')
                suc.option_add("*Font","궁서 15")
                lab1=Label(suc,text="성공적으로 저장했습니다.",width='40',height='12')
                lab1.pack()
                suc.mainloop()


        def begin():
            for i in range(5):
                ent[i].insert(0,myClass.name[i+1])

        def Fexcept():
            if ept[0]!="":
                for i in range(len(ept)):
                    if myClass.cur<=int(ept[i])<=myClass.cur+4:
                        j=int(ept[i])-myClass.cur
                        lab[j].configure(state='disabled')
                        ent[j].configure(state='disabled')
                        myClass.cur_ept.append(j)
    
    cur=0
    for i in range(cur,cur+5):
        lab[i]=Label(sel1_2,text=str(i+1)+"번")
        ent[i]=Entry(sel1_2,bd=0,disabledbackground='#12fb0c')
        lab[i].pack(anchor='nw',pady=(7,0),padx=(330,0))
        ent[i].pack(anchor='ne',pady=(7,0),padx=(0,350))
    myClass.begin()
    s_btn=Button(sel1_2)
    s_btn.config(text="저장")
    s_btn.config(command=myClass.save)    
    n_btn=Button(sel1_2)
    n_btn.config(text="다음으로 -->")
    n_btn.config(command=myClass.next)
    n_btn.pack(anchor='s',pady=(10,0))
    b_btn=Button(sel1_2)
    b_btn.config(text="<-- 이전으로")
    b_btn.config(command=myClass.bef)
    b_btn.pack(anchor='s',pady=(10,0))
    
    sel1_2.mainloop()



    
def rand_seat(main):
    destroy(main)
    sel2=Tk()
    sel2.title("rand_seat")
    sel2.geometry("1000x600")
    sel2.configure(bg='#12fb0c')
    sel2.option_add("*Font","궁서 30")
    global stu_num,stu_ept,desk_num

    home(sel2)

    lab=Label(sel2,text="자리 배치",width='20',height='3')
    lab.pack(pady=(10,30))
    
    def color():
        def sd_get_save():
            global stu_num,stu_ept,desk_num
            Red=(ent1.get()).split(',')
            Orange=(ent3.get()).split(',')
            Yellow=(ent2.get()).split(',')
            Green=(ent4.get()).split(',')
            col_stu=['0' for i in range(int(stu_num))]
            if Red[0]!='':
                for i in range(len(Red)):
                    cur=Red[i]
                    col_stu[int(cur)-1]='R'
            if Orange[0]!='':
                for i in range(len(Orange)):
                    cur=Orange[i]
                    col_stu[int(cur)-1]='O'
            if Yellow[0]!='':
                for i in range(len(Yellow)):
                    cur=Yellow[i]
                    col_stu[int(cur)-1]='Y'
            if Green[0]!='':
                for i in range(len(Green)):
                    cur=Green[i]
                    col_stu[int(cur)-1]='G'
            f_ran=open("range.txt",'r')
            store=[ ]
            store=f_ran.readlines()
            if len(store)==3:
                store[2]=store[2]+'\n'
                store.append('')
            elif len(store)==2:
                store.append('\n')
                store.append('')
            f_ran.close()
            store[3]=(','.join(col_stu))
            f_ran=open("range.txt",'w')
            for i in range(len(store)):
                f_ran.writelines(store[i])
            print(store)
            f_ran.close()
            suc=Tk()
            suc.title("success")
            suc.geometry("300x100")
            suc.configure(bg='#12fb0c')
            suc.option_add("*Font","궁서 15")
            lab1=Label(suc,text="성공적으로 저장했습니다.",width='40',height='12')
            lab1.pack()
            suc.mainloop()

        destroy(sel2)
        sel2_1=Tk()
        sel2_1.title("Seat_Color")
        sel2_1.geometry("1000x600")
        sel2_1.configure(bg='#12fb0c')
        sel2_1.option_add("*Font","궁서 25")
        home(sel2_1)

        

        lab1=Label(sel2_1,text="Red(','로 구분)",width='20')
        lab1.pack()
        ent1=Entry(sel2_1)
        #ent1.insert(0,stu_num)
        ent1.pack(pady=(5,15))

        lab3=Label(sel2_1,text="Orange(','로 구분)",width='20')
        lab3.pack(pady=(15,0))
        ent3=Entry(sel2_1)
        #ent3.insert(0,stu_ept)
        ent3.pack(pady=(5,15))

        lab2=Label(sel2_1,text="Yellow(','로 구분)",width='20')                                            
        lab2.pack(pady=(15,0))
        ent2=Entry(sel2_1)
        #ent2.insert(0,desk_num)
        ent2.pack(pady=(5,15))

        lab4=Label(sel2_1,text="Green(','로 구분)",width='20')                                            
        lab4.pack(pady=(15,0))
        ent4=Entry(sel2_1)
        #ent4.insert(0,desk_num)
        ent4.pack(pady=(5,15))

        btn1=Button(sel2_1)
        btn1.config(text="저장")
        btn1.config(command=sd_get_save)
        btn1.pack(pady=30)
        sel2_1.mainloop()


    def random():
        destroy(sel2)
        sel2_2=Tk()
        sel2_2.title("random")
        sel2_2.geometry("1000x600")
        sel2_2.configure(bg='#12fb0c')
        sel2_2.option_add("*Font","궁서 16")
        global stu_num,stu_ept,desk_num
        id=0
        ept_check=stu_ept.split(',')
        f_ran=open("range.txt")
        store=[ ]
        store=f_ran.readlines()
        if ept_check[0]=='':
            ept_len=0
        else:
            ept_len=len(ept_check)
        seat_state=[1 for i in range(int(stu_num)-ept_len)]
        if len(store)==3:
            col_store=['0' for i in range(int(stu_num))]
        elif len(store)==2:
            col_store=['0' for i in range(int(stu_num))]
        else:
            col_store=store[3].split(',')
        f_ran.close()
        
        
        desk_store=['0'for i in range(int(stu_num)-ept_len)]
        def col_chan(fid):
            
            #D->R->O->Y->G->N->D
            if desk_store[fid]=='0':
                seat[fid].config(bg='red')
                desk_store[fid]='R'
            elif desk_store[fid]=='R':
                seat[fid].config(bg='#ff7f00')
                desk_store[fid]='O'
            elif desk_store[fid]=='O':
                seat[fid].config(bg='yellow')
                desk_store[fid]='Y'
            elif desk_store[fid]=='Y':
                seat[fid].config(bg='green')
                desk_store[fid]='G'
            elif desk_store[fid]=='G':
                del_app(fid)
                desk_store[fid]='N'
            elif desk_store[fid]=='N':
                del_app(fid)
                desk_store[fid]='0'
            
        def del_app(fid):
            if seat_state[fid]==1:
                seat_state[fid]=0
                seat.append('')
                desk_store.append('0')
                seat_state.append(1)
                #print(len(seat)-1,fid)
                seat[len(seat)-1]=Button(sel2_2,text=len(seat),width='5',height='2',bd='0')
                seat[len(seat)-1].grid(column=(len(seat)-1)%int(desk_num)+1,row=((len(seat)-1)//int(desk_num))+1,padx='30',pady='15')
                seat[len(seat)-1].config(command=partial(col_chan,fid=len(seat)-1))
                seat[fid].config(text='',bg='#12fb0c')
            else:
                seat_state[fid]=1
                del seat_state[len(seat_state)-1]
                seat[len(seat)-1].grid_forget()
                del seat[len(seat)-1]
                del desk_store[len(desk_store)-1]
                seat[fid].config(text=fid+1,bg='SystemButtonFace')
        

        



        




        def DnC():
            destroy(sel2_2)
            fir_sel()
        btn=Button(sel2_2,text="Home",command=DnC,width='8',height='3')
        btn.grid(row='0',column='0')


        #print('1')
        MAX=math.ceil((int(stu_num)-ept_len)/int(desk_num))
        seat=[0 for i in range(int(stu_num)-ept_len)]
        for i in range(MAX):
            for j in range(int(desk_num)):
                if j==math.ceil(int(desk_num)/2):
                    mid_lab=Label(sel2_2,text='교탁',width='8',height='3',bg='#964b00')
                    mid_lab.grid(row='0',column=j)
                id=i*int(desk_num)+j
                seat[i*int(desk_num)+j]=Button(sel2_2,text=str(id+1),width='5',height='2',bd='0')     #현재 책상 번호:i*int(desk_num)+j+1
                seat[i*int(desk_num)+j].grid(column=j+1,row=i+1,padx='30',pady='15')
                seat[id].config(command=partial(col_chan,fid=id))
                if i*int(desk_num)+j+1>=int(stu_num)-ept_len:        #int(stu_num)-ept_len: 학생수
                    break
        sD_list=[ ]
        sR_list=[ ]
        sO_list=[ ]
        sY_list=[ ]
        sG_list=[ ]
        def seat_rand():
            print(len(col_store))
            for i in range(int(stu_num)):
                if str(i+1) in ept_check:
                    continue
                elif col_store[i]=='0':
                   sD_list.append(i+1)
                elif col_store[i]=='R':
                   sR_list.append(i+1)
                elif col_store[i]=='O':
                   sO_list.append(i+1)
                elif col_store[i]=='Y':
                   sY_list.append(i+1)
                elif col_store[i]=='G':
                   sG_list.append(i+1)

            
            rand_desk=[ ]
            i=0
            name=[None for i in range(1,int(stu_num)+1)]           
            f_name=open("name.txt",'r') 
            for i in range(int(stu_num)):          
                name[i]=f_name.readline().strip("\n")
            f_name.close()
            i=0
            while True:
                #print('1')
                if i>=len(desk_store):
                    break
                Crand=0
                if desk_store[i]=='N':
                    Crand=None
                elif desk_store[i]=='0':
                   Crand=rand.choice(sD_list)
                elif desk_store[i]=='R':
                    Crand=rand.choice(sR_list)
                elif desk_store[i]=='O':
                    Crand=rand.choice(sO_list)
                elif desk_store[i]=='Y':
                    Crand=rand.choice(sY_list)
                elif desk_store[i]=='G':
                    Crand=rand.choice(sG_list)
                if Crand not in rand_desk or Crand==None:
                    #print(Crand)
                    rand_desk.append(Crand)
                    i+=1
                    

            for i in range(len(rand_desk)):
                if rand_desk[i]!=None:
                    id=str(rand_desk[i])
                    seat[i].config(text=id+'\n'+name[int(id)-1])
                    #seat[i].config(font=('궁서',16))
                
            seat_save(rand_desk)
        def seat_save(rand_desk):
            f_seat=open("seat.txt",'w')
            for i in range(len(rand_desk)):
                f_seat.write(str(rand_desk[i])+',')
            f_seat.close()
            """
            cnt=0              
            for i in range(math.ceil(len(rand_desk)/int(desk_num))):        
                for j in range(int(desk_num)):                       
                    f_seat.write(str(rand_desk[i*int(desk_num)+j]))          
                    for k in range(5-len(str(rand_desk[i*int(desk_num)+j]))):        #k반복, 다시 출력할 때 그대로 출력할거라서 줄 맞추기
                        f_seat.write(" ")           #" "을 seat.txt에 입력
                        cnt+=1                          #여기서도 마찬가지로 카운트
                        if cnt>=len(rand_desk):                #여기서도 카운트 >= 학생수 면
                            f_seat.close()
                            return 0 
                        f_seat.write('\n')                  #\n을 seat.txt에 입력
                """        
        """
        btn1=Button(sel2_2)
        btn1.config(text="저장")
        btn1.config(command=seat_save)
        btn1.grid(row=MAX+2,column=math.ceil(int(desk_num)/3),pady='50')
        """

        btn2=Button(sel2_2)
        btn2.config(text="추첨",width='5',height='2')
        btn2.config(command=seat_rand)
        btn2.grid(row=MAX+2,column=(math.ceil(int(desk_num)/3))*2)
        sel2_2.mainloop()

                



    #선택지
    #1: 자리 색깔 설정
    btn1=Button(sel2)
    btn1.config(text='자리 색깔 설정')
    btn1.config(command=color)
    btn1.pack(pady=30)
    

    #2: 랜덤 자리 배치
    btn2=Button(sel2)
    btn2.config(text='랜덤 자리 배치')
    btn2.config(command=random)
    btn2.pack(pady=30)
    sel2.mainloop()






#메인

ran_path=os.getcwd()+'\\range.txt'      #os.getcwd는 파일의 현 위치를 문자열 형태로 리턴, 문자열+문자열=문자열이 합쳐짐,range.txt(학생 수, 책상의 가로 개수, 제외 학생 번호, 번호 별 색깔)의 경로
seat_path=os.getcwd()+'\\seat.txt'      #seat.txt(현재 자리 배치를 한 줄로)의 경로   
name_path=os.getcwd()+'\\name.txt'      #name.txt(학생들의 이름을 번호 순으로 나옆)의 경로

if(setting(ran_path,seat_path,name_path)==False):
    stu_ept,stu_num,desk_num=None
else:
    stu_num,desk_num,stu_ept=(setting(ran_path,seat_path,name_path).split(sep=' '))
fir_sel()   #거의 모든 기능을 함
