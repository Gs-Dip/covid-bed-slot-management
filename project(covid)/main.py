
 
import json
from flask import Flask,redirect,render_template,request,flash,session  
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from flask_mail import Mail
#mydatabase connection
app=Flask(__name__)
app.secret_key="password"

#akhane json file ta open kora hoyeche....admin login ar jonno
with open('config.json','r') as c:
    params=json.load(c)["params"]


#akhane flask-mail ke configure kora hoyeche------
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'], #json file a amar paramiter ache gmail-user  name
    MAIL_PASSWORD=params['gmail-password']
    
)
mail=Mail(app)  





#this is for getting the unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Userinfo.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dipdip2020@localhost/covid'
db=SQLAlchemy(app) #akhane sqlAlchemy diye amar database connect kora hoyche


class Test(db.Model): #test hocche amar covid database ar akta table ar nam akhane table ar nam ar porthom letter ta boro hater dite hobe
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))



class Userinfo(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(45),unique=True)   
    email=db.Column(db.String(45)) 
    dob=db.Column(db.String(1000))


class Hospital_user(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(45))   
    email=db.Column(db.String(45)) 
    password=db.Column(db.String(1000))


class Hospital_data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(50),unique=True)   
    hname=db.Column(db.String(50)) 
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer) 

class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(50))   
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)  
    querys=db.Column(db.String(50)) 
    date=db.Column(db.String(50))    


class Booking_patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(45),unique=True)   
    bedtype=db.Column(db.String(45)) 
    hcode=db.Column(db.String(45))
    spo2=db.Column(db.Integer)
    pname=db.Column(db.String(45))
    pphone=db.Column(db.Integer)
    paddress=db.Column(db.String(70))        

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/usersignup',methods=['GET','POST'])
def usersignup():
    if request.method=="POST":
        srfid=request.form.get('srf')
        email=request.form.get('email')
        dob=request.form.get('dob') #ata login ar somoy password hishebe dite hobe
        #print(srfid,email,dob) akhane locally terminal aa dekha hocche je amra from theke input gulo pacchi ki na
        encriptpassword=generate_password_hash(dob)  #password ke encript kora hoyeche...jate kore user ar password admin na dekhte pare
        #user aage thekei signup kora ache ki na ta chack korar jonno(user validation)
        user=Userinfo.query.filter_by(srfid=srfid).first()
        Useremail=Userinfo.query.filter_by(email=email).first()
        if user or Useremail:
            flash("Srf or Email already taken","warning")
            return render_template("usersignup.html")



        new_user=db.engine.execute(f"INSERT INTO `userinfo` (`srfid`,`email`,`dob`) VALUES ('{srfid}','{email}','{encriptpassword}') ")
        flash("Signup Success!!! Please Login","success")
        return render_template("userlogin.html")

    return render_template("usersignup.html") 

 
    

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method=="POST":
        srfid=request.form.get('srf')
        dob=request.form.get('dob')
        
        user=Userinfo.query.filter_by(srfid=srfid).first() #akhane amar userinfo table theke filter hobe srfid prothome and user login srfid fild a je value ta debe oita jodi userinfo table ar srfid collam ar sathe mele tahole  oi row ar sob akhane user variable ar moddhe store hobe

        if user and check_password_hash(user.dob,dob): #akhane bolahocche amar user variable ar moddhe je dob ta ache tar sathe jodi login dob value match kore tahole niche jabe 
            login_user(user)
            flash("Login Success!!!","info")
            return render_template("index.html")

        else:
            flash("something went wrong please try again!!!","danger") #ai message ta messege.html receive korbe 
            return render_template("userlogin.html") 
            
               
    return render_template("userlogin.html")  



@app.route('/hospitallogin',methods=['GET','POST'])
def hospitallogin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        
        userhos=Hospital_user.query.filter_by(email=email).first() #akhane amar userinfo table theke filter hobe srfid prothome and user login srfid fild a je value ta debe oita jodi userinfo table ar srfid collam ar sathe mele tahole  oi row ar sob akhane user variable ar moddhe store hobe

        if userhos and check_password_hash(userhos.password,password): #akhane bolahocche amar user variable ar moddhe je dob ta ache tar sathe jodi login dob value match kore tahole niche jabe 
            login_user(userhos)
            flash("Login Success!!!","info")
            return render_template ("index.html")

        else:
            flash("something went wrong please try again!!!","danger") #ai message ta messege.html receive korbe 
            return render_template("hospitallogin.html") 
            
               
    return render_template("hospitallogin.html")   
   



@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')

        if(username==params['user'] and password==params['password']):
            session['user']=username
            flash("Login Success","info")
            return render_template("addHosUser.html")

        else:
            flash("Login Failed!!!","danger")

                 
    return render_template("adminlogin.html") 
    


#user logout---------------------------------
@app.route('/logout')       

def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return render_template("userlogin.html")


#admin logout-----------------------------------------
@app.route('/adminlogout')       

def adminlogout():
    session.pop('user')
    flash("Admin Logout SuccessFul","primary")
    return render_template("adminlogin.html")




@app.route('/addHospitalUser',methods=['GET','POST'])
def addHospitalUser():
    
    if('user' in session and session['user']==params['user']): #ai route a shudhu admin chara kew jete parbe na
        
        if request.method=="POST": 
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password') #ata login ar somoy password hishebe dite hobe
            encriptpassword=generate_password_hash(password)  #password ke encript kora hoyeche...jate kore user ar password admin na dekhte pare
        #user aage thekei signup kora ache ki na ta chack korar jonno(user validation)
            hcode=hcode.upper()
            Useremail=Hospital_user.query.filter_by(email=email).first()
            if  Useremail:
               flash("email is already taken","warning")
               return render_template("addHosUser.html")
             


            db.engine.execute(f"INSERT INTO `hospital_user` (`hcode`,`email`,`password`) VALUES ('{hcode}','{email}','{encriptpassword}') ")
        
            mail.send_message ('COVID CARE CENTER', sender=params['gmail-user'],recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Information Are:\n Email Address:{email}\nPassword:{password} \n\nHospital Code: {hcode} \n Do Not Share Your Password \n\n\n Thank You.." ) # COVID CARE CENTER aita hocche mail ar subject r params hoccche amar config.json file ar akta paramiter........ai messege system ta lekhar agee obosshoi google accoutn mane je gmail address theke ami mail pathabo sheitake config.json file a set kore nite hobe.......tar por Manage your Google Account a giye security te giye Less secure app access ai option ta chalu kore dite hobe ta na hole messege sent korbe na  


            flash("data sent and inserted successfully","warning")
            return render_template("addHosUser.html")

    else:
        flash("login and tryagain","warning") #admin chara kono general user jodi ai route a jawar chesta kore tahole ai messege na show korbe 
        return render_template("adminlogin.html") 



@app.route('/hospitalinfo',methods=['GET','POST'])
def hospitalinfo():
     
    email=current_user.email
    posts=Hospital_user.query.filter_by(email=email).first()
    code=posts.hcode
    postdata=Hospital_data.query.filter_by(hcode=code).first() 

    if request.method=="POST":

        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        normalbed=request.form.get('normalbed')
        hicubed=request.form.get('hicubed')
        icubed=request.form.get('icubed')
        vbed=request.form.get('ventbed')
        hcode=hcode.upper()

        user=Hospital_user.query.filter_by(hcode=hcode).first()

        hospitaldata=Hospital_data.query.filter_by(hcode=hcode).first()

        if hospitaldata:
            flash("data is already present yon can update it","primary")
            return render_template("hospitaldata.html")
        
        if user:

            db.engine.execute(f"INSERT INTO `hospital_data` (`hcode`,`hname`,`normalbed`,`hicubed`,`icubed`,`vbed`) VALUES('{hcode}','{hname}','{normalbed}','{hicubed}','{icubed}','{vbed}')")
            flash("data is added successfully","primary") 
        
        else:
            flash("Hospital Code Not Exist","warning")
  
    return render_template("hospitaldata.html",postsdata=postdata)   


@app.route("/hedit/<string:id>",methods=['GET','POST'])    

@login_required
def hedit(id):
    if request.method=="POST":
    
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        normalbed=request.form.get('normalbed')
        hicubed=request.form.get('hicubed')
        icubed=request.form.get('icubed')
        vbed=request.form.get('ventbed')

        hcode=hcode.upper()

        db.engine.execute(f"UPDATE `hospital_data` SET `hcode`='{hcode}',`hname`='{hname}',`normalbed`='{normalbed}',`hicubed`='{hicubed}',`icubed`='{icubed}',`vbed`='{vbed}' WHERE `hospital_data`.`id`={id}")

        flash("Update Successfully","info")

        return redirect("/hospitalinfo")

    post=Hospital_data.query.filter_by(id=id).first()
    return render_template("hedit.html",post=post)



@app.route("/hdelete/<string:id>",methods=['GET','POST'])

@login_required
def hdelete(id):
    db.engine.execute(f"DELETE FROM `hospital_data` WHERE  `hospital_data`.`id`={id}")

    flash("Data Deleted Successfully","danger")
    return redirect("/hospitalinfo")
        


@app.route('/pdetails',methods=['GET'])
@login_required
def pdetails():
    srfid=current_user.srfid
    pd=Booking_patient.query.filter_by(srfid=srfid).first()

    return render_template("pdetails.html",pd=pd)


@app.route('/bookslot',methods=['GET','POST'])
@login_required
def bookslot():
    query=db.engine.execute(f"SELECT * FROM `hospital_data`")
    
    if request.method=="POST":
        srfid=request.form.get('srfid')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')
     
        check2=Hospital_data.query.filter_by(hcode=hcode).first()
        if not check2:
            flash("Hospital Code Not Exist","warning") 
        
        code=hcode

        dbb=db.engine.execute(f"SELECT * FROM `hospital_data` WHERE `hospital_data`.`hcode`='{code}' ")

        if bedtype=="NormalBed": #akhaner ai  NormalBed ta normalbed ar value hishebe set kora ache input aa...bookslot.html page a 
           for d in dbb:
               seat=d.normalbed
            #    print(seat) 
               ar=Hospital_data.query.filter_by(hcode=code).first()
               ar.normalbed=seat-1
               db.session.commit()

        
        elif bedtype=="H.I.C.UBed": #akhaner ai  NormalBed ta normalbed ar value hishebe set kora ache input aa...bookslot.html page a 
           for d in dbb:
               seat=d.hicubed
            #    print(seat) 
               ar=Hospital_data.query.filter_by(hcode=code).first()
               ar.hicubed=seat-1
               db.session.commit()
        

        elif bedtype=="I.C.UBed": #akhaner ai  NormalBed ta normalbed ar value hishebe set kora ache input aa...bookslot.html page a 
           for d in dbb:
               seat=d.icubed
            #    print(seat) 
               ar=Hospital_data.query.filter_by(hcode=code).first()
               ar.icubed=seat-1
               db.session.commit()
        

        elif bedtype=="VentilatorBed": #akhaner ai  NormalBed ta normalbed ar value hishebe set kora ache input aa...bookslot.html page a 
           for d in dbb:
               seat=d.vbed
            #    print(seat) 
               ar=Hospital_data.query.filter_by(hcode=code).first()
               ar.vbed=seat-1
               db.session.commit()
        
        else:
            pass


        check=Hospital_data.query.filter_by(hcode=hcode).first()
        if(seat>0 and check):
            res=Booking_patient(srfid=srfid,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress)
            db.session.add(res)
            db.session.commit()
            flash("Slot Is Booking Kindly Visit Hospital For Further Procedure","success")
        
        else:
            flash("Something Went Wrong","danger")


    return render_template("bookslot.html",query=query)


@app.route('/trigger')
def trigger():
    query=Trig.query.all()
    return render_template("trigger.html",query=query)



#testing database is connected or not
@app.route('/test')
def test():
    
    try:
        a=Test.query.all()
        print(a)
        return 'my database is connected'

    except Exception as e:
        print(e)
        return f'my database is not connected {e}' #jodi kono error ashe tahole ai messege tar (my database is not connected) pashe {e} mane error ta oo print korbe ba show korbe 



if __name__=='__main__':
    app.run(host="localhost",port=8900,debug=True)
