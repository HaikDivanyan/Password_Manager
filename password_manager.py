import sqlite3
#import sheets

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
         '| Password' + (' ' * (PASSWORD_LENGTH - len('Password'))) + '|')
    print('-'* WIDTH)
    for x in results:
        print('| ' + x[0]  + (' ' * (SERVICE_LENGTH - len(x[0]))), end='| ') #more ugly stuff
        print(x[1] + (' ' * (USERNAME_LEGNTH - len(x[1]))), end='| ')
        print(x[2] + (' ' * (PASSWORD_LENGTH - len(x[2]))), end='|\n')
        print('-'* WIDTH)


def addPassword():   # add a password to the database
    ADD_DATA_SQL = "INSERT INTO PASSWORDS VALUES (?,?,?)"
    _service_name = input('What service what you like to add?\n:')
    _service_name = _service_name.upper()
    _service_user = input('What is the username?\n:') #TODO verify that input <= max size
    _service_password = input('What is the password?\n:')
    user_info = [_service_name, _service_user, _service_password]
    c.execute(ADD_DATA_SQL, user_info)
    conn.commit()
    #sheets.add_to_sheets(_service_name, _service_user, _service_password)
    print('Infomration stored successfully!')

def viewPassword(): #view all passwords
    SORT_BY_KEY_SQL = "SELECT * FROM PASSWORDS ORDER BY SERVICE_NAME" #sorts them alphabetically by service name
    c.execute(SORT_BY_KEY_SQL)
    results = c.fetchall()
    displayInfo(results)

def managePasswords(): #manage/edit passwords
    viewPassword()
    choice = input('Which service would you like to modify/remove?\n:')
    choice = choice.upper()
    SEARCH_BY_KEY_SQL = "SELECT * FROM PASSWORDS WHERE SERVICE_NAME = ?"
    c.execute(SEARCH_BY_KEY_SQL, (choice,)) #TODO: check to see if service exists
    info = c.fetchall()
    displayInfo(info)
    action = input('tpye "d" to delete, or "m" to modify a password\n:')
    action = action.lower()
    while True:
        if action == 'd':
            DELETE_SQL = 'DELETE FROM PASSWORDS WHERE SERVICE_NAME = ?'
            c.execute(DELETE_SQL, (choice,))
            conn.commit()
            #sheets.delete_from_sheets(choice)
            print(choice + ' has been deleted!')
            break
        elif action == 'm':
            new_password = input('Please type the new password\n:')
            UPDATE_PASSWORD_SQL = 'UPDATE PASSWORDS SET USER_PASSWORD = ? WHERE SERVICE_NAME = ?'
            c.execute(UPDATE_PASSWORD_SQL, (new_password, choice,))
            conn.commit()
            #sheets.update_sheets(choice, new_password)
            print('Password updated!')
            break
        else:
             action = input('Error: type "d" to delete, or "m" to modify a password\n:')
    
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
        _input = input(':')

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
        elif _input != 'vp' and _input != 'ap' and _input != 'mp' and _input != 'q':
            print('Error: that is not a command.\n')  

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

