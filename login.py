def login():
    global name
    if(ENV=="dev"):
        if request.method == "POST":
            userid = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            query = db.Query(registration).filter(registration.number==userid, registration.password==password).first()
            if(query):
                name = db.Query(patients).get(patients.uuid==query.uuid)
                session['user'] = name
                session['logged_in'] = True
                session['role'] = ""
                return render_template('login.html', user=name,error="")    
            else:
                return render_template('login.html',error="Invalid Username Or Password")
    elif(ENV=='demo'):
        if(request.method == "POST"):
            userid = str(request.form.get("userid"))
            password = str(request.form.get("password"))
            if(userid==password):
                session['user'] = name
                session['logged_in'] = True
                session['role'] = ""
                return render_template('login.html', user=name,error="")    
    return render_template('login.html', user=name,error="")