from flask import Flask, render_template,request,session,flash
import sqlite3 as sql
import os
import pandas as pd
app = Flask(__name__)

@app.route('/')            
def home():
   return render_template('index.html')

@app.route('/gohome')
def homepage():
    return render_template('index.html')

@app.route('/enternew')
def new_user():
   return render_template('signup.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['Name']                         #registration of new user
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            with sql.connect("diauser.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO diabetes(name,phono,email,username,password)VALUES(?, ?, ?, ?,?)",(nm,phonno,email,unm,passwd))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/userlogin')
def user_login():
   return render_template("login.html")

@app.route('/adminlogin')
def login_admin():
    return render_template('login1.html')

@app.route('/logindetails',methods = ['POST', 'GET'])
def logindetails():
    if request.method=='POST':                          #authentication of existing users
            usrname=request.form['username']
            passwd = request.form['password']

            with sql.connect("diauser.db") as con:
                cur = con.cursor()
                cur.execute("SELECT username,password FROM diabetes where username=? ",(usrname,))
                account = cur.fetchall()

                for row in account:
                    database_user = row[0]
                    database_password = row[1]
                    if database_user == usrname and database_password==passwd:
                        session['logged_in'] = True
                        return render_template('home.html')
                    else:
                        flash("Invalid user credentials")
                        return render_template('login.html')



@app.route('/predictinfo')
def predictin():
   return render_template('info.html')






@app.route('/predict1',methods = ['POST', 'GET'])
def predcrop():
    global comment1
    if request.method == 'POST':
        comment1 = request.form['comment1']       #getting the input from the form
        comment2 = request.form['comment2']
        comment3 = request.form['comment3']
        comment4 = request.form['comment4']
        comment5 = request.form['comment5']
        comment6 = request.form['comment6']
        comment7 = request.form['comment7']
        comment8 = request.form['comment8']
        comment9 = request.form['comment9']
        comment10 = request.form['comment10']
        comment11 = request.form['comment11']

        length = len(comment2)    #finding length of username
        digcount = 0
        for char in comment2:     #finding the number of digits in the username
            if char.isdigit():
                digcount += 1

        ratio = digcount/length    #finding ratio
        import math
        ratio = round(ratio,2)

        namelength = len(comment4)    #length of the account name
        digcount2 = 0
        for char in comment4:         #no of digits
            if char.isdigit():
                digcount2 += 1
        
        ratio2 = digcount2/namelength  #ratio
        ratio2 = round(ratio2,2)


        data1 = comment1
        data2 = ratio
        data3 = comment3
        data4 = ratio2
        data5 = comment5
        data6 = comment6
        data7 = comment7
        data8 = comment8
        data9 = comment9
        data10 = comment10
        data11 = comment11
        print(data1)
        print(data2)
        print(data3)
        print(data4)
        print(data5)
        print(data6)
        print(data7)
        print(data8)
        print(data9)
        print(data10)
        print(data11)

        import pandas as pd
        import random
        df = pd.read_csv("insta_train.csv")
        df.to_csv("train.csv", header=False, index=False)        #removing heading and index in the dataset
        dataset = pd.read_csv("train.csv")
        X = dataset.iloc[:, 0:10].values                  #storing first 10 columns in x

        Y = dataset.iloc[:, 11].values                    #storing the last column in y
        

        from sklearn.model_selection import train_test_split
        #test_size = 0.2 means only 2% of the whole dataset is sent for testing
        X_train, X_test1, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 5)  


        print('X_test_data', X_test1)


        from sklearn.svm import SVC
        classifier = SVC(kernel = 'linear', random_state = 0)   #kernal transforms data into linear form
        classifier.fit(X_train, Y_train)                    #fit the svm model according to training data
        X_test = [[data1, data2, data3, data4,data5,data6, data7, data8, data9, data10]]       #giving our input to model
        Y_pred = classifier.predict(X_test)            #store result in Y_pred 
        print('Y_pred_test',Y_pred)

        Y_pred1 = classifier.predict(X_test1)         #predicting for test data
        print('Y_pred',Y_pred)


        from sklearn.metrics import confusion_matrix,classification_report
        cm = confusion_matrix(Y_test, Y_pred1)           #comparing test data prediction result with original result
        print("\n",cm)

        print(classification_report(Y_test,Y_pred1))        #to calculate precision,recall, F1 score 

        iclf = SVC(kernel='linear', C=1).fit(X_train, Y_train)   
        accuracy2=((iclf.score(X_test1, Y_test))*100)   #finding training accuracy
        print("accuracy=",accuracy2)

        # import matplotlib.pyplot as plt

        # x = [0, 1, 2]
        # y = [accuracy2, 0, 0]
        # plt.title('Accuracy2')
        
        if Y_pred[0] == 1:
            response1= 'Fake Profile'
            print('Fake Profile')
        else:
            response1 = 'Real Profile'
            print('Real Profile')
        
        import csv

        data = [[data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, Y_pred[0]]]
        
        with open('insta_train.csv', 'a', newline='') as csvfile:
    # Create a CSV writer object
            writer = csv.writer(csvfile)

    # Append the data to the CSV file
            writer.writerows(data)


    return render_template('resultpred.html', prediction=response1, prediction1 = accuracy2)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
