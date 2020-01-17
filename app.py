from flask import Flask,render_template,request,redirect,session,url_for
from werkzeug.utils import secure_filename
import hashlib
import sqlite3
import os
conn=sqlite3.connect('python.sqlite', check_same_thread=False)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
cursor = conn.cursor()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
############decorator##########


# @app.route("/register",methods=['POST','GET']) #decorator
# def register():
#     if request.method == "POST":
#         name=request.form['name']
#         password=request.form['password']
        
#         hash_object=hashlib.sha1(password.encode("utf8"))
#         hex_dig = hash_object.hexdigest()
#         insertQuery="INSERT INTO users(name,hash) values(?,?)"

#         cursor.execute(insertQuery,(name,hex_dig))

#         conn.commit()
#         return redirect("/login")

#         # return "record saved successfully <br/>name ="+name+"<br/> Password ="+hex_dig
#     else :
#         return render_template("backend/formelement.html")

@app.route("/login",methods=['POST','GET']) #decorator
def login():
    errors = {}
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        if username == "":
                errors['username'] = "Username is empty"

        if password == "":
                errors['password'] = "Password is empty"

        if len(errors) != 0:
                return render_template("backend/login.html", errors=errors)

        hash_object=hashlib.sha1(password.encode("utf8"))
        hex_dig = hash_object.hexdigest()
        selectQuery="Select * from users where username=? and hash= ?"
        cursor.execute(selectQuery,(username,hex_dig))
        data=cursor.fetchone()
        if data != None:
            session["user_id"]=data[0]
            session["name"]=data[1]
            session["success"]="1"
            return redirect("/dashboard.html")
        else:
            errors['user'] = "User does not exist"
            return render_template("backend/login.html", errors = errors)
    else :
        return render_template("backend/login.html", errors=errors)

@app.route("/dashboard.html") #decorator
def dasboard():
        if 'user_id' not in session.keys():
                return redirect("/login")
        # if session["user_id"]:
        #         return render_template("backend/dashboard.html")
        else:
                return render_template("backend/dashboard.html")

                # return redirect("/")

@app.route("/logout") #decorator
def logout():
    session.clear()
    return redirect("/")


    # # # # post CRUD # # #
@app.route("/user/create",methods=['POST','GET']) #decorator
def user_create():
    errors = {}
    if request.method == "POST":
        name=request.form['name']
        uname=request.form['username']
        password=request.form['password']
        if name == "":
                errors['name'] = "Name is empty"

        if uname == "":
                errors['username'] = "username is empty"
        if password == "":
                errors['password'] = "password is empty"
        if len(errors) != 0:
                return render_template("backend/user_create.html", errors=errors)
        hash_object=hashlib.sha1(password.encode("utf8"))
        hex_dig = hash_object.hexdigest()

        insertQuery="INSERT INTO users(name,username,hash) values(?,?,?)"

        cursor.execute(insertQuery,(name,uname,hex_dig))

        conn.commit()
        session["success"]="Data inserted successfully"
        # return redirect("/user/"+str(session["user_id"]))

        return redirect("/user")

        # return "record saved successfully <br/>name ="+name+"<br/> Password ="+hex_dig
    else :
        if 'user_id' not in session.keys():
                return redirect("/login")
        
        return render_template("backend/user_create.html",errors = errors)

@app.route("/user") #decorator
def user_list():
    errors={}
    if 'user_id' not in session.keys():
        return redirect("/login")
    selectQuery="Select * from users"
    cursor.execute(selectQuery)
    data=cursor.fetchall()
    if session["success"] != "1":
        errors['success'] = session["success"]
        session["success"]=""
    # print(data)
    return render_template("backend/user_list.html",value=data,errors = errors)

@app.route("/user/<id>/edit",methods=['POST','GET']) #decorator
def user_edit(id):
    if request.method == "POST":
        name=request.form['name']
        uname=request.form['username']
        updateQuery="UPDATE users set name=?,username=? where id= "+id

        cursor.execute(updateQuery,(name,uname))

        conn.commit()
        session["success"]="Data updated successfully"
        # return redirect("/user/"+str(session["user_id"]))

        return redirect("/user")

    else:
        if 'user_id' not in session.keys():
                return redirect("/login")
        selectQuery="Select * from users where id= "+id
        cursor.execute(selectQuery)
        data=cursor.fetchone()
        # print(data)
        return render_template("backend/user_edit.html",value=data)
@app.route("/user/<id>/delete",methods=['POST','GET']) #decorator
def user_delete(id):
    if request.method == "POST":
        # id=request.form['id']
        # print(id)
        deleteQuery="Delete from users where id= "+id
        cursor.execute(deleteQuery)
        conn.commit()

        session["success"]="Data Deleted successfully"
        # return redirect("/user/"+str(session["user_id"]))
        return redirect("/user")


@app.route("/education/create",methods=['POST','GET']) #decorator
def education_create():
    errors = {}
    if request.method == "POST":
        title=request.form['title']
        college=request.form['college']
        college_address=request.form['college_address']
        description=request.form['description']
        status=request.form['status']
        if title == "":
                errors['title'] = "title is empty"

        if college == "":
                errors['college'] = "college is empty"
        if college_address == "":
                errors['college_address'] = "college address is empty"
        if description == "":
                errors['description'] = "descriptionis empty"
        if len(errors) != 0:
                return render_template("backend/education_create.html", errors=errors)
        insertQuery="INSERT INTO educations(title,college,college_address,description,status,created_by) values(?,?,?,?,?,?)"

        cursor.execute(insertQuery,(title,college,college_address,description,status,session['user_id']))

        conn.commit()
        session["success"]="Data inserted successfully"
        # return redirect("/education/"+str(session["education_id"]))

        return redirect("/education")

        # return "record saved successfully <br/>name ="+name+"<br/> Password ="+hex_dig
    else :
        if 'user_id' not in session.keys():
                return redirect("/login")
        return render_template("backend/education_create.html",errors = errors)

@app.route("/education") #decorator
def education_list():
    errors={}
    if 'user_id' not in session.keys():
        return redirect("/login")
    selectQuery="Select * from educations"
    cursor.execute(selectQuery)
    data=cursor.fetchall()
    if session["success"] != "1":
        errors['success'] = session["success"]
        session["success"]=""
    # print(data)
    return render_template("backend/education_list.html",value=data,errors = errors)

@app.route("/education/<id>/edit",methods=['POST','GET']) #decorator
def education_edit(id):
    errors = {}
    if request.method == "POST":
        title=request.form['title']
        college=request.form['college']
        college_address=request.form['college_address']
        description=request.form['description']
        status=request.form['status']
        if title == "":
                errors['title'] = "title is empty"

        if college == "":
                errors['college'] = "college is empty"
        if college_address == "":
                errors['college_address'] = "college address is empty"
        if description == "":
                errors['description'] = "descriptionis empty"
        if len(errors) != 0:
                selectQuery="Select * from educations where id= ?"
                cursor.execute(selectQuery,(id))
                data=cursor.fetchone()
                return render_template("backend/education_edit.html",value=data ,errors=errors)
        
        

        
        updateQuery="UPDATE educations set title=?,college=?,college_address=?,description=?,status=? where id= "+id

        cursor.execute(updateQuery,(title,college,college_address,description,status))

        conn.commit()
        session["success"]="Data updated successfully"
        # return redirect("/user/"+str(session["user_id"]))

        return redirect("/education")

    else:
        if 'user_id' not in session.keys():
                return redirect("/login")
        selectQuery="Select * from educations where id= "+id
        cursor.execute(selectQuery)
        data=cursor.fetchone()
        # print(data)
        return render_template("backend/education_edit.html",value=data,errors=errors)
@app.route("/education/<id>/delete",methods=['POST','GET']) #decorator
def education_delete(id):
    if request.method == "POST":
        # print(id)
        deleteQuery="Delete from educations where id= "+id
        cursor.execute(deleteQuery)
        conn.commit()
        session["success"]="Data Deleted successfully"
        # return redirect("/user/"+str(session["user_id"]))
        return redirect("/education")
@app.route("/project/create",methods=['POST','GET']) #decorator
def project_create():
    target=os.path.join(APP_ROOT,'static/uploaded_image')
    print(target)
    errors = {}
    if request.method == "POST":
        title=request.form['title']
        # image=request.form['image']
        link=request.form['link']
        rank=request.form['rank']
        image_title=request.form['image_title']
        status=request.form['status']
        if title == "":
                errors['title'] = "title is empty"

        if link == "":
                errors['link'] = "link is empty"
        if rank == "":
                errors['rank'] = "Rank is empty"
                # ########################
        if not os.path.isdir(target):
                os.mkdir(target)
        for upload in request.files.getlist('image'):
                filename=upload.filename
                destionation="/".join([target,filename])
                upload.save(destionation)
                print(upload)
        file=request.files['image']
        # ?\###############

        if len(errors) != 0:
                return render_template("backend/project_create.html", errors=errors)
        insertQuery="INSERT INTO projects(title,image,link,rank,status,image_title) values(?,?,?,?,?,?)"

        cursor.execute(insertQuery,(title,file.filename,link,rank,status,image_title))

        conn.commit()
        session["success"]="Data inserted successfully"
        # return redirect("/education/"+str(session["project_id"]))

        return redirect("/project")

        # return "record saved successfully <br/>name ="+name+"<br/> Password ="+hex_dig
    else :
        # if 'user_id' not in session.keys():
        #         return redirect("/login")
        return render_template("backend/project_create.html",errors = errors)

@app.route("/project") #decorator
def project_list():
    errors={}
    if 'user_id' not in session.keys():
        return redirect("/login")
    selectQuery="Select * from projects"
    cursor.execute(selectQuery)
    data=cursor.fetchall()
    if session["success"] != "1":
        errors['success'] = session["success"]
        session["success"]=""
    # print(data)
    return render_template("backend/project_list.html",value=data,errors = errors)

@app.route("/project/<id>/edit",methods=['POST','GET']) #decorator
def project_edit(id):
    errors = {}
    if request.method == "POST":
        title=request.form['title']
        image=request.form['image']
        link=request.form['link']
        rank=request.form['rank']
        image_title=request.form['image_title']
        status=request.form['status']
        if title == "":
                errors['title'] = "title is empty"
        if link == "":
                errors['link'] = "link is empty"
        if rank == "":
                errors['rank'] = "Rank is empty"
        if len(errors) != 0:
                selectQuery="Select * from projects where id= ?"
                cursor.execute(selectQuery,(id))
                data=cursor.fetchone()
                return render_template("backend/project_edit.html",value=data ,errors=errors)
        
        updateQuery="UPDATE projects set title=?,image=?,link=?,rank=?,status=?,image_title=? where id= "+id

        cursor.execute(updateQuery,(title,image,link,rank,status,image_title))

        conn.commit()
        session["success"]="Data updated successfully"
        # return redirect("/user/"+str(session["user_id"]))

        return redirect("/project")

    else:
        if 'user_id' not in session.keys():
                return redirect("/login")
        selectQuery="Select * from projects where id= "+id
        cursor.execute(selectQuery)
        data=cursor.fetchone()
        # print(data)
        return render_template("backend/project_edit.html",value=data,errors=errors)
@app.route("/project/<id>/delete",methods=['POST','GET']) #decorator
def project_delete(id):
    if request.method == "POST":
        # print(id)
        deleteQuery="Delete from projects where id= "+id
        cursor.execute(deleteQuery)
        conn.commit()
        session["success"]="Data Deleted successfully"
        # return redirect("/user/"+str(session["user_id"]))
        return redirect("/project")




@app.route("/message") #decorator
def message_list():
    errors={}
    if 'user_id' not in session.keys():
        return redirect("/login")
    selectQuery="Select * from messages order by status ASC "
    cursor.execute(selectQuery)
    data=cursor.fetchall()
    if session["success"] != "1":
        errors['success'] = session["success"]
        session["success"]=""
    # print(data)
    return render_template("backend/message_list.html",value=data,errors=errors)
@app.route("/message/<id>/detail") #decorator
def message_detail(id):
        if 'user_id' not in session.keys():
                return redirect("/login")
        # print(id)
        updateQuery="UPDATE messages set status=1 where id= "+id
        cursor.execute(updateQuery)
        conn.commit()
        selectQuery="Select * from messages where id = "+id
        cursor.execute(selectQuery)
        data=cursor.fetchone()
        # session["success"]="Data updated successfully"
        # return redirect("/user/"+str(session["user_id"]))
        return render_template("backend/message_detail.html",value=data)
@app.route("/message/<id>/delete",methods=['POST','GET']) #decorator
def message_delete(id):
    if request.method == "POST":
        # id=request.form['id']
        # print(id)
        deleteQuery="Delete from messages where id= "+id
        cursor.execute(deleteQuery)
        conn.commit()

        session["success"]="Data Deleted successfully"
        # return redirect("/message/"+str(session["message_id"]))
        return redirect("/message")
# # # # frontend work
@app.route("/",methods=['POST','GET']) 
def index():
    errors={}
    
    if request.method == "POST":
        name=request.form['name']
        email=request.form['email']
        subject=request.form['subject']
        message=request.form['message']

        if name == "":
                errors['name'] = "name is empty"

        if email == "":
                errors['email'] = "email is empty"
        if subject == "":
                errors['subject'] = "subject is empty"
        if message == "":
                errors['message'] = "message is empty"
        if len(errors) != 0:
                return render_template("frontend/index.html", errors=errors)
        

        insertQuery="INSERT INTO messages(name,email,subject,message,status) values(?,?,?,?,0)"

        cursor.execute(insertQuery,(name,email,subject,message))

        conn.commit()
        session["msg"]="Data inserted successfully"
        # return redirect("/education/"+str(session["education_id"]))

        return redirect("/")

        # return "record saved successfully <br/>name ="+name+"<br/> Password ="+hex_dig
    else :
        selectQuery="Select * from educations where status = 1"
        cursor.execute(selectQuery)
        data=cursor.fetchall()

        getQuery="Select * from projects where status = 1 order by rank"
        cursor.execute(getQuery)
        project_data=cursor.fetchall()
        # print(data)
        return render_template("frontend/index.html",value=data,project=project_data,errors = errors)

if __name__=="__main__":
    app.secret_key=os.urandom(12)
    app.run(debug=True)