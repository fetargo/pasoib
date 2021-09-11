import AccessDB, Login, os
#' ' - no access
def checkAccess(userID, path):
    userAccess = AccessDB.selectRules(userID, path, Login.con)
    return userAccess

def checkAccessMand(userLevel, path):
    userAccess, relogin = AccessDB.selectRuleMand(userLevel, path, Login.con)
    return userAccess, relogin

def initOSRules():
    cur = Login.con.cursor()
    cur.execute('SELECT "path" FROM "Access"')
    files = cur.fetchall()
    if len(files) != 0:
        for file in files:
            os.chmod(file[0], 000)
        print("OS access init")
    else:
        print("There's no rules for files") 

if __name__ == "__main__":
    print(checkAccess(0, "/Users/fetargo", "x"))
    print(checkAccess(0, "/Users/tester", "x"))
    print(checkAccess(0, "/Users/tester/ban", "x"))