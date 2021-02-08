import sqlite3
import sheets

#c.fetchall() returns array of tuples

SERVICE_LENGTH = 30 #max sizes for input fields
USERNAME_LEGNTH = 30
PASSWORD_LENGTH = 30

DATABASE_NAME = 'password.db'
conn = sqlite3.connect(DATABASE_NAME) #connects to database
c = conn.cursor() #use this to write queries

def createDB():
    create_table_sql = '''CREATE TABLE IF NOT EXISTS PASSWORDS 
                        (SERVICE_NAME TEXT PRIMARY KEY NOT NULL,
                        USER_NAME TEXT NOT NULL,
                        USER_PASSWORD TEXT NOT NULL)'''
    c.execute(create_table_sql)

def displayInfo(results): #display all the info selected
    WIDTH = PASSWORD_LENGTH + USERNAME_LEGNTH + SERVICE_LENGTH + 7
    print('-'* WIDTH)
    print('| Service Name' + (' ' * (SERVICE_LENGTH - len('Service Name'))) +    #ugly but it works well when you change legnths
         '| Username' + (' ' * (USERNAME_LEGNTH - len('Username'))) +         
         '| Password' + (' ' * (PASSWORD_LENGTH - len('Password'))) + '|') #TODO use printf stye to replace
    print('-'* WIDTH)
    for x in results:
        print('| ' + x[0]  + (' ' * (SERVICE_LENGTH - len(x[0]))), end='| ') #more ugly stuff
        print(x[1] + (' ' * (USERNAME_LEGNTH - len(x[1]))), end='| ')
        print(x[2] + (' ' * (PASSWORD_LENGTH - len(x[2]))), end='|\n')
        print('-'* WIDTH)

def validateInput(name, size):
    while len(name) > size:
        name = input(f'this field can be no longer than {size} characters, please enter again\n:')
    return name

def addPassword():   # add a password to the database
    ADD_DATA_SQL = "INSERT INTO PASSWORDS VALUES (?,?,?)"

    _service_name = input('What service what you like to add?\n:').strip().upper()
    if len(_service_name) > SERVICE_LENGTH:
        _service_name = validateInput(_service_name, SERVICE_LENGTH)
    _service_name = _service_name.upper().strip()  

    _service_user = input('What is the username?\n:').strip()
    if len(_service_user) > USERNAME_LEGNTH:
        _service_user = validateInput(_service_user, USERNAME_LEGNTH)

    _service_password = input('What is the password?\n:')
    if len(_service_password) > PASSWORD_LENGTH:
        _service_password = validateInput(_service_password, PASSWORD_LENGTH)

    user_info = [_service_name, _service_user, _service_password]
    c.execute(ADD_DATA_SQL, user_info)
    conn.commit()
    print('Infomration stored successfully!')
    
def viewPassword(): #view all passwords
    SORT_BY_KEY_SQL = "SELECT * FROM PASSWORDS ORDER BY SERVICE_NAME" #sorts them alphabetically by service name
    c.execute(SORT_BY_KEY_SQL)
    results = c.fetchall()
    displayInfo(results)
    data = list(map(list, results))
    sheets.updateSheet(data)

def itemExists(choice):
    while True:
        c.execute('SELECT 1 FROM PASSWORDS WHERE SERVICE_NAME=? LIMIT 1', (choice,)) #returns [(1,)] for True or [(0,)] for False
        choice_exists = (c.fetchone() is not None) #converts to True or False
        if choice_exists: 
            return choice
        else:
            choice = input(f'"{choice}" does not exist in your database, please enter the name again or "b" to go back to the menu\n:').strip().upper()
            if choice == 'B':
                return False

def managePasswords(): #manage/edit passwords
    viewPassword()
    choice = input('Which service would you like to modify/remove?\n:').strip().upper()
    valid_input = itemExists(choice)
    if valid_input == False: #user chose to go to menu
        return
    action = input('tpye "d" to delete, or "m" to modify a password\n:').strip().upper()
    while True:
        if action == 'D':
            DELETE_SQL = 'DELETE FROM PASSWORDS WHERE SERVICE_NAME = ?'
            c.execute(DELETE_SQL, (valid_input,))
            conn.commit()
            print(valid_input + ' has been deleted!')
            break
        elif action == 'M':
            new_password = input('Please type the new password\n:')
            UPDATE_PASSWORD_SQL = 'UPDATE PASSWORDS SET USER_PASSWORD = ? WHERE SERVICE_NAME = ?'
            c.execute(UPDATE_PASSWORD_SQL, (new_password, valid_input,))
            conn.commit()
            print('Password updated!')
            break
        else:
             action = input('Error: type "d" to delete, or "m" to modify a password\n:').strip().upper()
    
def resetPasswords(): #erases all entries, but keeps the table
    print('Are you sure you want to reset all passwords?')
    check = input('type "YES" to proceed or anything else to go back\n:')
    if check == 'YES':
        RESET_DATABASE_SQL = 'DELETE FROM PASSWORDS'
        c.execute(RESET_DATABASE_SQL)
        conn.commit()
        print('Password Manager has been reset!')
    else:
        return

def user_interface(): 
    while True:
        print("~"*25)
        print('vp = view passwords')
        print("ap = add a password")
        print("mp = manage passwords")
        print("rp = reset ALL passwords")
        print("q  = quit program")
        print('~'*25)
        _input = input(':').strip().lower()

        if _input == 'vp':
            viewPassword()
        elif _input == 'ap':
            addPassword()
        elif _input == 'mp':
            managePasswords()
        elif _input == 'rp':
            resetPasswords()
        elif _input == 'q':
            return False
        else:
            print('Error: that is not a command.\n')

        viewPassword()



if __name__ == '__main__':
    PASSWORD = '123456'
    while True:
        login = input('Enter the password: ')
        if login == PASSWORD:
            break
        else:
            print('Incorrect, try again')

    createDB()    
    print('\nWhat would you like to do?\n')
    user_interface()