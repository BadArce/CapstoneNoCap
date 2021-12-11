import bcrypt
import sqlite3
from datetime import datetime

connection = sqlite3.connect('A&F.db')
cursor = connection.cursor()

class User:
    def __init__ (self,first_name,last_name,phone, email, password, hire_date, privilege, createtime = 0,activebool = 1, id = -1):
        self.id = id
        self.fn = first_name
        self.ln = last_name
        self.phone = phone
        self.hd = hire_date
        self.priv = privilege
        self.email = email
        self.__password = password
        self.created = createtime
        self.active = activebool
        self.list = (self.id, self.fn, self.ln, self.phone, self.email, self.__password, self.hd, self.priv, self.created, self.active)




def login():
    global entry
    loginfo = input('Please enter your email: ').lower()
    lc = cursor.execute("SELECT * FROM Users WHERE email=?",(loginfo,)).fetchone();
    if lc == None:
        print('\n I\'m sorry, no user with that email found.\n')
        return
    lc = list(lc)
    password = input('Please enter your password: ').encode("utf-8")
    hashed = lc[5]
    if bcrypt.checkpw(password,hashed) and lc[9] == 1:
        entry = True
        lccount = 0
        for x in lc:
            if x == None:
                lc[lccount] = ''
            lccount += 1
        cu = User(lc[1],lc[2],lc[3],lc[4],lc[5],lc[6],lc[7],lc[8],lc[9],lc[0],)
        print(f'\nWelcome {cu.fn} (User ID: {cu.id})\n')
        return cu
    elif bcrypt.checkpw(password,hashed) and lc[9] == 0:
        print ("I'm sorry, your account is not active. Please contact your administrator.\n")
        print ("Exiting program")
        entry = 'You lose, busta'
        
    else:
        print("Input invalid, please try again.")
    # print('End of logn')


user_header = f'{"User ID":<9}|{"First Name":<16} {"Last Name":<16} {"Phone #":<15} {"Email Address":<32} {"Hire Date":<20} {"Priv.":<5} {"Acct. Creation Date":<20} {"Active":<6}\n---------|---------------- ---------------- --------------- -------------------------------- -------------------- ----- -------------------- ------'


def view_user(user):
    print(user_header)
    if isinstance(user[0], (list,tuple)):
        for i in user:
            if i[9] >= 1:
                act = 'Yes'
            else:
                act = 'No'
            print(f'{i[0]!s:<9} {i[1]!s:<16} {i[2]!s:<16} {i[3]!s:<15} {i[4]!s:<32} {i[6]!s:<20} {i[7]!s:<5} {i[8]!s:<20} {act:<6}')
    else:
        if user[9] >= 1:
                act = 'Yes'
        else:
                act = 'No'
        print(f'{user[0]!s:<9} {user[1]!s:<16} {user[2]!s:<16} {user[3]!s:<15} {user[4]!s:<32} {user[6]!s:<20} {user[7]!s:<5} {user[8]!s:<20} {act:<6}')


def man_view_user():
    minno = cursor.execute('SELECT user_id from users ORDER by user_id ASC').fetchone();
    maxno = cursor.execute('SELECT user_id from users ORDER by user_id DESC').fetchone();
    choice = input ("\nWhat would you like to see?\n  1) View all users.\n  2) View specific users\n  3) view a range of users\n  9) return to menu\n\n> ")
    if choice == '1':
        users = cursor.execute('SELECT * from users ORDER by user_id ASC').fetchall();
        view_user(users)
    elif choice == '2':
        users = []
        while True:
            choice = input('\nPlease enter the user_id you would like to see (type "Q" to finish): ')
            if choice == 'Q':
                break
            else:
                try:
                    choice = int(choice)
                    usr = cursor.execute('SELECT * fROM Users WHERE user_id=?',(choice,)).fetchone();
                    if usr == None:
                        print("\nUser not found.")
                    else:
                        print('\nUser found.')
                        users.append(usr)
                except:
                    print('Sorry, input not understood.)')
        if users == []:
            print('\nNo users selected. Returning to menu.\n')
            return
        else:
            view_user(users)
    elif choice == '3':
        users = []
        startno = input('Please type the starting (lower) number: ')
        endno = input('Please type the end (high) number: ')
        try:
            startno = int(startno)
            endno = int(endno)
        except:
            print('Input not valid.')
            return
        if startno > endno:
            print('Input not valid.')
            return
        for x in range (startno,endno+1):
            usr = cursor.execute('SELECT * fROM Users WHERE user_id=?',(x,)).fetchone();
            if usr == None:
                pass
            else:
                users.append(usr)
        if users == []:
            print('\nNo users selected. Returning to menu.\n')
            return
        else:
            view_user(users)
        
    elif choice == '9':
        return
    else:
        print('Sorry, input not understood.')
        return



def find_user():
    search = input("\nPlease type the first or last name you wish to search by: ")
    search = f"%{search}%"
    found = cursor.execute("SELECT * FROM Users where first_name LIKE ? OR last_name LIKE ?",(search,search)).fetchall();
    if found == [] or found == None:
        print("I'm sorry, no users found.")
        return
    print(found)
    view_user(found)

def ed_or_del():
    options = {
        1 : 'edit',
        2 : 'delete'
    }
    choice = input('\nWould you like to edit or delete a record?\n  1) edit\n  2) delete\n\nPlease type the corresponding number, or type "Q" to return to menu: ')
    if choice == 'Q' or choice == 'q':
        return
    try:
        choice = int(choice)
        choice = options[choice]
    except:
        print("Input invalid.")
        return
    if choice == 'delete':
        tables= {
            1 : 'Users',
            2 : 'Assessment_Results'
        }
        choice = input('\nWhat kind of record would you like to delete?\n  1) Users\n  2) Assessment Results\n\nPlease type the corresponding number, or type "Q" to return to menu: ')
        if choice == 'Q' or choice == 'q':
            return
        try:
            choice = int(choice)
            choice = tables[choice]
        except:
            print("Input invalid.")
            return
        if choice == 'Users':
            delchoice = input('Please type the user ID: ')
            check = cursor.execute('SELECT * FROM Users WHERE user_id = ?', (delchoice,)).fetchone();
            if check == None:
                print('User not found.')
                return
            else:
                cursor.execute('Update Users SET active = 0 WHERE user_id = ?',(delchoice))
                connection.commit()
        else:
            delchoice1 = input('Please type the user ID: ')
            delchoice2 = input('Please type the assessment ID: ')
            check1 = cursor.execute("SELECT taken_date,score FROM Assessment_Results WHERE assessment_id = ? and user_id = ?",(delchoice2,delchoice1)).fetchall();
            if check1 == []:
                print('No matches found.')
                return
            elif len(check1) == 1:
                save = input('\nConfirm deletion? "y" for yes or "n" for no: ').lower()
                if save == 'y':
                    cursor.execute('DELETE FROM Assessment_Results WHERE assessment_id = ? and user_id = ?',(delchoice2,delchoice1))
                    connection.commit()
                    print('\nChanges saved.\n')
                    return
                else:
                    print('\nChanges not saved.\n')
                    return
            else:
                print(f"{'no.':<4}|{'Date taken':<20}|{'score':>6}")
                print(f"{'*'*4}|{'*'*20}|{'*'*6}")
                counter=0
                for i in check1:
                    print(f'{counter:<4}|{i[0]:<20}|{i[1]:>6}')
                    counter +=1
                selection = input("Please type the number of the record you wish to delete: ")
                try:
                    selection = int(selection)
                    cursor.execute('DELETE FROM Assessment_Results WHERE assessment_id = ? aND user_id = ? AND taken_date = ? AND score = ?',(delchoice2,delchoice1,check1[selection]))
                    save = input('\nConfirm deletion? "y" for yes or "n" for no: ').lower()
                except:
                    print('An error occured.')
                    return
                save = input('\nConfirm deletion? "y" for yes or "n" for no: ').lower()
                if save == 'y':
                    connection.commit()
                    print('\nChanges saved.\n')
                    return
                else:
                    print('\nChanges not saved.\n')
                    return

                


    else:
        edit_record()  
   

def edit_user(user = None):
    while user == None:
        choice = input('\nPlease type the user ID number of the user you wish to edit (type "q" to return to menu): ')
        if choice == 'q' or choice == 'Q':
            return
        try:
            choice = int(choice)
            check = cursor.execute('SELECT first_name FROM Users WHERE user_id = ?', (choice,)).fetchone();
            if check != None:
                user = choice
            else:
                print('Invalid input. Please try again.')
        except:
            print('Invalid input. Please try again.')
    while True:
        selection = input("Which would you like to update:\n - [1] First Name\n - [2] Last Name\n - [3] Phone\n - [4] Email\n - [5] Password\n - [6] Return to menu\n\n> ")
        if selection == '1':
            change = input(f"What is the new first name for user #{user}: ")
            sql_update = "UPDATE Users SET first_name = ? WHERE user_id = ?"
            values  = (change,user)
            cursor.execute(sql_update,values)
        elif selection == '2':
            change = input(f"What is the new last name for user #{user}: ")
            sql_update = "UPDATE Users SET last_name = ? WHERE user_id = ?"
            values  = (change,user)
            cursor.execute(sql_update,values)
        elif selection == '3':
            change = input(f"What is the new phone number for user #{user}: ")
            sql_update = "UPDATE Users SET phone = ? WHERE user_id = ?"
            values  = (change,user)
            cursor.execute(sql_update,values)
        elif selection == '4':
            change = input(f"What is the new email address for user #{user}: ")
            change_check = input("Please retype the new email: ")
            sql_update = "UPDATE Users SET email = ? WHERE user_id = ?"
            values  = (change,user)
            if change == change_check:
                cursor.execute(sql_update,values)
            else:
                print("I'm sorry, input did not match.")
        elif selection == '5':
            change = input(f"What is the new password for user #{user}: ")
            change_check = input("Please retype the new password: ")
            sql_update = "UPDATE Users SET password = ? WHERE user_id = ?" 
            if change == change_check:
                change = change.encode('utf-8')
                salt = bcrypt.gensalt()
                change = bcrypt.hashpw(change,salt)
                values  = (change,user)
                cursor.execute(sql_update,values)
            else:
                print("I'm sorry, input did not match.")
        elif selection == '6':
            return
        Continue = input('Continue editing this account? Type "y" for yes and "n" for no:  ').lower()
        if Continue == 'y':
            pass
        elif Continue != 'n':
            print('Sorry, input not understood.')
        if Continue != 'y':
            save = input('\nSave changes? "y" for yes or "n" for no: ').lower()
            if save == 'y':
                connection.commit()
                print('\nChanges saved.\n')
                return
            else:
                print('\nChanges not saved.\n')
                return



def user_comp_overview(userid = "need input"):
    if userid == "need input":
        user_select = input ("Please enter the user ID of the person's record you would like to see: ")
        try:
            userid = int(user_select)
        except:
            print("Invalid input, please try again.")
    top = cursor.execute("SELECT competency_id from Competencies ORDER BY competency_id DESC;").fetchone();
    results = [['Comp. ID.', 'Competency', 'Score', 'Date taken', 'Manager ID'],["---------",'------------------------------','-------','--------------------','----------']]
    for x in range (1, top[0] + 1):
        result = cursor.execute('SELECT c.competency_id, c.name, ar.score, ar.taken_date, ar.manager_id FROM Competencies c, Assessment_Results ar WHERE c.competency_id = ar.competency_id AND user_id = ? AND c.competency_id = ? ORDER BY taken_date DESC', (userid,x)).fetchone();
        if result == None:
            compname = cursor.execute("SELECT name FROM Competencies WHERE competency_id=?",(x,)).fetchone();
            result = [x,compname[0],0,"NO DATA",'']
        results.append(result)
    for i in results:
        print(f'{i[0]:<9} {i[1]:<30} {i[2]:<7} {i[3]:<20} {i[4]:<10} ')


def view_history(user = None,single = 1):
    while user == None:
        choice = input('\nPlease type the user ID number of the user you wish to edit (type "q" to return to menu): ')
        if choice == 'q' or choice == 'Q':
            return
        try:
            choice = int(choice)
            check = cursor.execute('SELECT first_name FROM Users WHERE user_id = ?', (choice,)).fetchone();
            if check != None:
                user = choice
            else:
                print('\nInvalid input. Please try again.')
        except:
            print('\nInvalid input. Please try again.')
    comp1 = 0
    while comp1 == 0:    
        comp = input('\nPlease input the competency ID that you\'d like to see the history of: ')
        try:
            comp1 = int(comp)
            test = cursor.execute('SELECT name FROM Competencies WHERE competency_id = ?',(comp1,)).fetchone();
            if test == None:
                print('Invalid input, please try again.')
                return
        except:
            print('Invalid input, please try again.')
            return
        records = cursor.execute('SELECT ar.taken_date, ar.assessment_id, at.name, at.description, co.name ,ar.score,ar.manager_id FROM Assessment_Results ar, Assessments at, Competencies co WHERE ar.assessment_id = at.assessment_id AND ar.competency_id = co.competency_id AND at.competency_id = co.competency_id AND ar.competency_id = ? AND ar.user_id = ? ORDER BY taken_date DESC', (comp1,user)).fetchall();
        hdr = ["Date", "Assmnt. ID.","Assmnt. Name", "Assmnt. Desc.", "Competency", "Score", "Mngr. ID."]
        bar = '*'
        print(f'{hdr[0]:<19} {hdr[1]:<10} {hdr[2]:<30} {hdr[3]:<35} {hdr[4]:<20} {hdr[5]:<5} {hdr[6]:<9}')
        print(f'{bar*19} {bar*10} {bar*30} {bar*35} {bar*20} {bar*5} {bar*9}')
        for i in records:
            print(f'{i[0]:<19} {i[1]:<10} {i[2]:<30} {i[3]:<35} {i[4]:<20} {i[5]:<5} {i[6]:<9}')
    return


def user_terminal(name):
    options = {
        1 : "view_user(cu.list)",
        2 : "user_comp_overview(cu.id)",
        3 : "view_history(cu.id)",
        4 : "edit_user(cu.id)",
        9 : "logout()"  
    }
    
    print(f'\n\nWhat would you like to do {name}?\n')
    choice = input(f'''
      - 1) View your user information
      - 2) View your competency overview
      - 3) View your assessment history
      - 4) Edit your personal information
      - 9) Log out and quit program
      
    Please type the number of your selection.\n\n> ''')
    try:
        choice = int(choice)
    except:
        print("Error: Input invalid, please try again.")
    
    try:
        exec(options[choice])
    except:
        print('\n Input invalid, please try again.')
    
def man_terminal(name):
    options = {
        1: 'user_terminal(cu.fn)',
        2: 'man_terminal_sub(cu.fn)',
        9: 'logout()'
    }

    print(f'\n\nWhat would you like to do {name}?\n')
    choice = input(f'''
      - 1) View personal commands
      - 2) View advanced (manager) commands.
      - 9) Log out and quit program
      
    Please type the number of your selection.\n\n> ''')
    try:
        choice = int(choice)
    except:
        print("Error: Input invalid, please try again.")
    
    try:
        exec(options[choice])
    except:
        print('\n Input invalid, please try again.')

def comp_report():
    comps = [('Comp. ID.','Competency','Creation Date'),('---------','------------------------------','--------------------')]
    results = cursor.execute('SELECT * from Competencies').fetchall();
    counter = 0
    for i in results:
        if i[0]> counter:
            counter = i[0]
        comps.append(i)
    for i in comps:
        print(f'{i[0]:<9} {i[1]:<30} {i[2]:<20}')

    choice = input('For which competency would you like a report?\n\nPlease type the competency ID number: ')
    try:
        choice = int(choice)
    except:
        print("\ninvalid input. Returning to menu.")
    
    # users = cursor.execute('SELECT user_id from Users').fetchall();
    # us=[]
    # for i in users:
    #     us.append(i[0])
    recs = cursor.execute('SELECT u.user_id,u.first_name,u.last_name, ar.* FROM Users u LEFT OUTER JOIN Assessment_Results ar ON c.user_id = ar.user_id WHERE ar.competency_id = ? GROUP BY user_id', (choice,)).fetchall();
    
def add_record():
    tables= {
        1 : 'Users',
        2 : 'Competencies',
        3 : 'Assessments',
        4 : 'Assessment_Results'
    }
    choice = input('\nTo which table would you like to add a new record?\n  1) Users\n  2) Competencies\n  3) Assessments\n  4) Assessment Results\n Please type the corresponding number, or type "Q" to return to menu: ')
    if choice == 'Q' or choice == 'q':
        return
    try:
        choice = int(choice)
        choice = tables[choice]
    except:
        print("Input invalid.")
        return
    columns = cursor.execute("SELECT cid,name FROM PRAGMA_TABLE_INFO('?')",(choice,)).fetchall();
    keys = []
    cols = []
    for i in columns:
        keys.append(i[0])
        cols.append(i[1])
    
    changes = []
    print('Please fill all fields, if necessary leave them blank.')
    for i in keys:
        if i == 0 and choice != 'Assessment_Results':
            change = None
            changes.append(change)
        if cols[i] == 'creation_date':
            change = datetime.now()
            changes.append(change)
        elif cols[i] == 'password':
            change = input(f'What is the new record\'s {cols[i]}: ')
            salt = bcrypt.gensalt()
            change = change.encode('utf-8')
            change = bcrypt.hashpw(change,salt)
            changes.append(change)
        elif cols[i] == 'manager_id':
            change = cu.id
            changes.append(change)
        elif cols[i] == 'active':
            change = 1
            changes.append(change)
        elif cols[i] == 'competency_id' and i == 3:
            change = cursor.execute('SELECT competency_id FROM Assessments WHERE assessment_id = ?'(changes[0],)).fetchone();
            if change == None:
                change = input(f'What is the new record\'s {cols[i]}: ')
                changes.append(change)
        else:
            change = input(f'What is the new record\'s {cols[i]}: ')
            changes.append(change)
    try:
        cols = tuple(cols)
        cursor.execute(f'INSERT INTO Users {cols} VALUES ?',(changes))
    except:
        print('An error occured, please try again later. If error persists, please contact your administrator.')
        return
    connection.commit()
    return
    



def edit_record():
    tables= {
        1 : 'Users',
        2 : 'Competencies',
        3 : 'Assessments',
        4 : 'Assessment_Results'
    }
    choice = input('\nTo which table would you like to add a new record?\n  1) Users\n  2) Competencies\n  3) Assessments\n  4) Assessment Results\n Please type the corresponding number, or type "Q" to return to menu: ')
    if choice == 'Q' or choice == 'q':
        return
    try:
        choice = int(choice)
        choice = tables[choice]
    except:
        print("Input invalid.")
        return
    keys = []
    cols = []
    columns = cursor.execute("SELECT cid,name FROM PRAGMA_TABLE_INFO('?')",(choice,)).fetchall();
    for i in columns:
        keys.append(i[0])
        cols.append(i[1])
    print(f"{'no.':<4}|{'Date taken':<15}")
    print(f"{'*'*4}|{'*'*15}")
    for x in range(0,len(cols)):
        print(f"{x:<4}|{cols[x]:<15}")
    selection = input("Please type the number of the data you wish to edit: ")
    try:
        selection = int(selection)
    except:
        print('\nInput invalid, please try again.')
        return

    print("\nIm sorry. currently all we are capable of editind are the users. \nPlease delete the old record and create a new one.")
    return

    




add_record()

def man_terminal_sub(name):
    options = {
        1 : 'man_view_user()',
        2 : 'find_user()',
        3 : "user_comp_overview()",
        4 : 'comp_report()',
        5 : "view_history()",
        6 : 'add_record()',
        7 : 'ed_or_del()',
        # 8 : export/import reports
        9 : 'return'
        
    }
    print(f'\n\nWhat would you like to do {name}?\n')
    choice = input(f'''
      - 1) View lists of user information
      - 2) View specific users
      - 3) View competency information of a specific user
      - 4) View a specific competency report
      - 5) View a user's assessment history
      - 6) Add(create) a record.
      - 7) Edit or delete a record.
      - 8) *Export function not functional currently*
      - 9) Log out and quit program
      
    Please type the number of your selection.\n\n> ''')
    try:
        choice = int(choice)
    except:
        print("Error: Input invalid, please try again.")
    
    try:
        exec(options[choice])
    except:
        print('\n Input invalid, please try again.')

def logout():
    global entry
    global cu
    selection = input('\nWould you like to quit?\n  - type "y" for yes\n  - type "n" to return to the main menu\n\n> ').lower()
    if selection =='y':
        del cu
        entry = False
        return
    elif input != 'n':
        print("Input invalid.")
        return


entry = False
while entry != True:
    cu = login()
    if entry == 'You lose, busta':
        break

while entry == True:
    if cu.priv <= 1:
        user_terminal(cu.fn)
    else:
        man_terminal(cu.fn)


# I'm so sorry.