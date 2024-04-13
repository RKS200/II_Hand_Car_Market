#Importing Libraries
import sqlite3,csv

#Defining Global Varibales
USER = 'admin'

#Defining Data Formatting Functions
createUser = lambda user,pin,phno : "insert into auth values('{}',{},{});".format(user,pin,phno)
def printDetails(data):
    data = data[0]
    print("\nRegNo: {}\nOwner: {}\nName: {}\nType: {}\nYear: {}\nPrice: {}".format(data[0],data[1],data[2],data[3],data[4],data[5]))
    print("Issues:")
    for i in eval(data[6]):
        print('*',i)
    cur.execute("select phno from auth where user = '{}';".format(data[1]))
    phno = cur.fetchall()[0][0]
    print("Contact:",phno)

#Estabilishing connection with the database
conn = sqlite3.connect("local.db")
cur = conn.cursor()

#Creating tables if not present
try:
    cur.execute("create table auth(user varchar(30) primary key,pin integer,phno integer unique);")
    cur.execute(createUser('admin','1234','NULL'))
    cur.execute("create table car(regno char(10) primary key,user varchar(30),name varchar(50),type varchar(20),year integer,price integer,issues varchar(1000),FOREIGN KEY (user) REFERENCES auth(user));")
    conn.commit()
except:
    pass

#Functions for authentication
def signIn(user,pin):
    cur.execute("select * from auth where user = '{}' and pin = {}".format(user,pin))
    if len(cur.fetchall()) == 1:
        return True
    else:
        False

def auth():
    global USER
    print('\n')
    print('*'*40)
    print("Authentication")
    print('*'*40)
    print("1.SignIn\n2.SignUp\n3.Exit")
    print('*'*40)
    ch = int(input("\n\n>>> Enter your Command(1-3): "))
    if ch == 1:
        user = input("\n>>> Enter Username: ")
        pin = int(input(">>> Enter PIN: "))
        if signIn(user,pin):
            USER = user
            print("SignIn Successful.")
        else:
            print("SignIn UnSuccessful.")
            auth()
    elif ch == 2:
        user = input("\n>>> Enter Username: ")
        pin = int(input(">>> Enter PIN: "))
        phno = int(input(">>> Enter Ph.no: "))
        cur.execute(createUser(user,pin,phno))
        conn.commit()
        if signIn(user,pin):
            USER = user
            print("SignUp Successful.")
        else:
            print("SignUp UnSuccessful.")
            auth()
    elif ch == 3:
        print('Thank you')
        exit()
    else:
        print("Invalid Command.")
        auth()

#Functions For User&admin operations
def insertCar():
    regno = input(">>> Enter Registration No(XX00XX0000): ")
    name = input(">>> Enter the Car Name(<Company name> <Model Name>): ")
    type = input('>>> Enter the Car Type: ')
    year = int(input('>>> Enter the year(xxxx): '))
    price = int(input('>>> Enter the price(Rs): '))
    issues = []
    while True:
        issues.append(input('>>> Enter the issues(One by One): '))
        if input('>>> Do you Want to Enter More?(y/n): ') in 'Nn': break
    try:
        cur.execute("""insert into car values('{}','{}','{}','{}',{},{},"{}");""".format(regno,USER,name,type,year,price,str(issues)))
        conn.commit()
        print("Data Inserting Successfull.")
    except:
        print("Data Inserting Unsuccessfull.\nMay be the car already exists.\nOr you are not following the specified Format.")

def removeCar():
    regno = input('>>> Enter Registration No(XX00XX0000): ')
    if USER == 'admin':
        cur.execute('select * from car where regno = "{}";'.format(regno))
    else:
        cur.execute('select * from car where regno = "{}" and user = "{}";'.format(regno,USER))
    d= cur.fetchall()
    if len(d) == 1:
        printDetails(d)
        if input('>>> Do you Want to Remove this above Car?(y/n): ') in 'Yy':
            cur.execute('delete from car where regno = "{}";'.format(regno))
            conn.commit()
            with open('removed.log','a') as file:
                file.write('delete from car where regno = "{}";\n'.format(regno))
            print("Car Removed Successfully.")
        else:
            print("Car is not Removed.Process UnSuccessfull.")
    else:
        print("Car is Removed.Process UnSuccessfull.\nCar dosen't exist.")

def modifyCar():
    regno = input('>>> Enter Registration No(XX00XX0000): ')
    if USER == 'admin':
        cur.execute('select * from car where regno = "{}";'.format(regno))
    else:
        cur.execute('select * from car where regno = "{}" and user = "{}";'.format(regno,USER))
    d= cur.fetchall()
    if len(d) == 1:
        printDetails(d)
        print('\n')
        print('*'*40)
        print('Modification')
        print('*'*40)
        print("1.Change Name\n2.Change Type\n3.Change Year\n4.Change Price\n5.Change Issues\n6.Cancel")
        print('*'*40)
        ch = int(input('\n\n>>> Enter your Choice(1-6): '))
        if ch == 1:
            name = input(">>> Enter the Car Name(<Company name> <Model Name>): ")
            cur.execute("update car set name = '{}' where regno = '{}';".format(name,regno))
            conn.commit()
        elif ch == 2:
            type = input('>>> Enter the Car Type: ')
            cur.execute("update car set type = '{}' where regno = '{}';".format(type,regno))
            conn.commit()
        elif ch == 3:
            year = int(input('>>> Enter the year(xxxx): '))
            cur.execute("update car set year = {} where regno = '{}';".format(year,regno))
            conn.commit()
        elif ch == 4:
            price = int(input('>>> Enter the price(Rs): '))
            cur.execute("update car set price = {} where regno = '{}';".format(price,regno))
            conn.commit()
        elif ch == 5:
            issues = []
            while True:
                issues.append(input('>>> Enter the issues(One by One): '))
                if input('>>> Do you Want to Enter More?(y/n): ') in 'Nn': break
            cur.execute("""update car set issues = "{}" where regno = '{}';""".format(issues,regno))
            conn.commit()
        elif ch == 6:
            pass
        else:
            print('Invalid Input')
            modifyCar()
    else:
        print("Car Modified UnSuccessfully.\nCar dosen't exist.")

def searchCar():
    cur.execute("select * from car;")
    totalData = len(cur.fetchall())
    print('\n')
    print('*'*40)
    print('Buy')
    print('*'*40)
    print("1.Search with RegNo\n2.Search by Name\n3.Search by Type\n4.Search by Year\n5.Search by Price\n6.Cancel")
    print('*'*40)
    ch = int(input('\n\n>>> Enter your Choice(1-6): '))
    if ch ==1:
        regno = input(">>> Enter Registration No(XX00XX0000): ")
        cur.execute("select * from car where regno = '{}';".format(regno))
        data = cur.fetchall()
        for i in data:
            printDetails([i])
        print("Loaded {} Details from {}".format(len(data),totalData))
    elif ch == 2:
        name = input(">>> Enter the Car Name(<Company name> <Model Name>): ")
        cur.execute("select * from car where name = '{}';".format(name))
        data = cur.fetchall()
        for i in data:
            printDetails([i])
        print("Loaded {} Details from {}".format(len(data),totalData))
    elif ch == 3:
        type = input('>>> Enter the Car Type: ')
        cur.execute("select * from car where type = '{}';".format(type))
        data = cur.fetchall()
        for i in data:
            printDetails([i])
        print("Loaded {} Details from {}".format(len(data),totalData))
    elif ch == 4:
        year = int(input('>>> Enter the year(xxxx): '))
        cur.execute("select * from car where year = {};".format(year))
        data = cur.fetchall()
        for i in data:
            printDetails([i])
        print("Loaded {} Details from {}".format(len(data),totalData))
    elif ch == 5:
        minPrice = int(input('>>> Enter the minimum price(Rs): '))
        maxPrice = int(input('>>> Enter the maximum price(Rs): '))
        cur.execute("select * from car where price between {} and {};".format(minPrice,maxPrice))
        data = cur.fetchall()
        for i in data:
            printDetails([i])
        print("Loaded {} Details from {}".format(len(data),totalData))
    elif ch == 6:
        pass
    else:
        print('Invalid Input')
        searchCar()

#Functions for admin operaions
def exportCSV():
    cur.execute("select regno,car.user,name,type,year,price,issues,phno from car,auth where car.user = auth.user;")
    l = cur.fetchall()
    with open('Exported.csv','w',newline = '')as f:
        w = csv.writer(f)
        w.writerow(['RegNo','Owner','Name','Type','Year','Price','Issues','Contact'])
        for i in l:
            issue = ''
            for j in eval(i[6]):
                issue += j+','
            issue = issue.strip(',')
            w.writerow([i[0],i[1],i[2],i[3],i[4],i[5],issue,i[7]])
    print('\nExported the data as "Exported.csv".')

#main Program starts here
auth()
while True:
    print('\n')
    print('*'*40)
    print('II Hand Cars Market')
    print('*'*40)
    print('1. Sell a Car\n2. Buy\n\n3. Remove a Car Details\n4. Modify a Car Details\n5. Exit')
    if USER == 'admin':
        print('\n6. Export as CSV')
        print('*'*40)
        ch = int(input('\n\n>>> Enter your Choice(1-6): '))
    else:
        print('*'*40)
        ch = int(input('\n\n>>> Enter your Choice(1-5): '))
    if ch == 1: insertCar()
    elif ch == 2: searchCar()
    elif ch == 3: removeCar()
    elif ch == 4: modifyCar()
    elif ch == 5: break
    elif ch == 6: exportCSV()
    else: print('Invalid Input')