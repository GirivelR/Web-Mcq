from flask import Flask,render_template,request,make_response,jsonify
import random
import pickle
import datetime,pytz
from teacherreg import Teacher
from studentsreg import Student

app = Flask(__name__)
app.secret_key='giri'
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/studentslogin')
def studentslogin():
    return render_template('studentslogin.html')
@app.route('/teacherslogin')
def teacherslogin():
    return render_template('teacherslogin.html',det='')

@app.route('/teachersdelete')
def teachersdelete():
    global tid
    return render_template('questions.html',det=tid+" Deleted")

@app.route('/teacherslogincheck',methods=['POST'])
def teacherslogincheck():
    if request.method=='POST':
        log=request.form
        t=Teacher(name=log['tname'],password=log['tpass']).login()
        global tid
        tid=t[1]
        if t[0]==1:
            return render_template('questions.html',det=t[1])
        return render_template('teacherslogin.html',det='Wrong')

@app.route('/teacherreginsert',methods=['POST'])
def teacherregclass():
    if request.method=='POST':
        teacherdet=request.form
        if teacherdet['pw']==teacherdet['rpw']:
            r=int(random.randrange(100000,1000000))
            Teacher(r,teacherdet['name'],teacherdet['pw'],teacherdet['sub']).insert()
            return render_template("home.html")
@app.route('/teacherreg')
def teacherreg():
    return render_template('teacherreg.html')
@app.route('/questionsupload',methods=['POST'])
def questionupload():
    if request.method=='POST':
        qus=request.form
        global tid
        li=[['/* here we will move asked (whether answered or not) questions */']]
        l=qus['message'].split('\r\n')
        for i in l:
            i=i.split('|')
            print(i[0].split(','))
            li.append([i[0].split(','),'false',int(i[1])])
        try:
            with open('questionup.txt','rb') as p:
                d=pickle.load(p)
                print(d)
                p.close()
            with open('questionup.txt','wb') as p:
                d[tid]=[qus['stime'],int(qus['duration']),li]
                print(d)
                pickle.dump(d,p)
                p.close()

        except Exception as e:
            return render_template('questions.html', qus="Questions not uploaded", det=tid)
        else:
            return render_template('questions.html', qus="Questions uploaded", det=tid)

@app.route('/studentsreginsert',methods=['POST'])
def studentsreginsert():
    if request.method=='POST':
        std=request.form
        Student(std['tid'],std['name'],std['cls'],std['pas'],std['sn']).insert()
        return render_template('home.html')

@app.route('/studentslogincheck',methods=['POST'])
def studentslogincheck():
    if request.method=='POST':
        stu=request.form
        global sn
        sn=stu['sname']
        s=Student(roll_name=stu['sname'],password=stu['spass']).login()
        if s[0] == 1:
            with open('questionup.txt','rb') as p:
                d=pickle.load(p)
                p.close()
            h,m=map(int,d[str(s[1])][0].split(':'))
            t=datetime.time(h,m)
            now=datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            n=now.strftime("%H:%M")
            a,b=map(int,n.split(':'))
            n=datetime.time(a,b)
            if m>30:
                h+=1
                m=m-30
            else:
                m+=30
            end=datetime.time(h,m)
            if str(s[1]) in d.keys():
                if n>=t and n<=end:
                    return render_template('quiz.html',ques=d[str(s[1])][2] ,dur=d[str(s[1])][1] , det=s[1])
                else:
                    return render_template('studentslogin.html', det='Test not started')
        return render_template('studentslogin.html', det='Wrong Details')

@app.route('/studentsreg')
def studentsreg():
    return render_template('stureg.html')
@app.route('/get_mark',methods=['POST'])
def get_mark():
    global sn
    req=request.get_json()
    Student(roll_name=sn,marks=req['mark']).marksupload()
    res=make_response(jsonify({"message":"Message received"}))
    return res



@app.route('/studentsdet',methods=['POST'])
def studentsdet():
    global tid
    l=Student(teacher_id=tid).display()
    return render_template('studentsdet.html',det=l)


if __name__ == '__main__':
   app.run(debug = True)