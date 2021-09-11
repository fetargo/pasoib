import psycopg2
# import os

def connectToDB():
    con = psycopg2.connect(
        database="rules",
        user="fetargo",
        password="1488",
        host="127.0.0.1",
        port="5432"    
    )
    print("Database opened successfully")
    return con


def selectOnlyUsers(con):
    cur = con.cursor()
    cur.execute('SELECT "Users"."username", "Users"."userID" FROM "Users"')
    users = cur.fetchall()
    if len(users) != 0:
        print("List of users found")
        return users
    else:
        print("Users not found")
        return None

def selectUsers(con, path):
    cur = con.cursor()
    cur.execute('SELECT "Users"."username", "Users"."userID", "Access"."access", "Access"."owner"' +
                ' FROM "Users", "Access" WHERE "Users"."userID" = "Access"."userID"' + 
                ' AND "Access"."path" = %(path)s', {'path':path})
    users = cur.fetchall()
    if len(users) != 0:
        print("List of users found", users)
        return users
    else:
        print("Users not found")
        return None

def selectRules(userID, path, con):
    cur = con.cursor()
    cur.execute('SELECT "access" FROM "Access"' + 
                ' WHERE "userID" = %(id)s' +
                ' AND "path" = %(path)s', {'id':userID, 'path':path})
    rules = cur.fetchall()
    if len(rules) != 0:
        print("Rule for path: " + path + " is " + rules[0][0])
        return rules[0][0]
    else:
        print("Rule for path: " + path + " not found")
        return "rwx"

def addRule(userID, path, access, con):
    cur = con.cursor()
    cur.execute('INSERT INTO "Access" ("userID", "path", "access") VALUES ' + 
                "(%(id)s, %(path)s, %(rule)s)", {'id':userID, 'path':path, 'rule':access})
    try:
        con.commit()
        print("Row added")
        print("AccessDB.addRule return code: 0")
        # os.system('sudo chown root ' + path)
        # os.system('sudo chmod 700 ' + path)
        return 0
    except:
        print("Row adding failed")
        print("AccessDB.addRule return code: 1")
        return 1

def updateRule(userID, path, access, con):
    cur = con.cursor()
    cur.execute('UPDATE "Access" SET "access" = %(rule)s' +
                ' WHERE "userID" = %(id)s AND "path" = %(path)s',
                {'id':userID, 'path':path, 'rule':access})
    try:
        con.commit()
        print("Rule updated")
        print("AccessDB.updateRule return code: 0")
        # os.system('sudo chown root ' + path)
        # os.system('sudo chmod 700 ' + path)
        return 0
    except:
        print("Rule update failed")
        print("AccessDB.updateRule return code: 1")
        return 1

def updatePath(pathBefore, pathAfter, con):
    if pathBefore == pathAfter:
        print("Path not updated")
        print("AccessDB.updatePath return code: 1")
        return 1
    paths = selectTemplatePath(pathBefore, con)
    cur = con.cursor()
    for path in paths:
        pathAfter = path[0].replace(pathBefore, pathAfter)
        cur.execute('UPDATE "Access" SET "path" = %(pathA)s' +
                    ' WHERE "path" = %(pathB)s',
                    {'pathA':pathAfter, 'pathB':pathBefore})
    try:
        con.commit()
        print("Path updated")
        print("AccessDB.updatePath return code: 0")
        return 0
    except:
        print("Path update failed")
        print("AccessDB.updatePath return code: 1")
        return 1

def setRule(userID, path, access, con):
    cur = con.cursor()
    cur.execute('SELECT "access" FROM "Access"' + 
                ' WHERE "userID" = %(id)s' +
                ' AND "path" = %(path)s', {'id':userID, 'path':path})
    rules = cur.fetchall()
    if len(rules) != 0:
        print("Rule for path: " + path + " is " + rules[0][0])
        errorcode = updateRule(userID, path, access, con)
    else:
        print("Rule for path: " + path + " not found")
        errorcode = addRule(userID, path, access, con)
    print("AccessDB.setRule return code: " + str(errorcode))

def selectTemplatePath(pth, con):
    cur = con.cursor()
    path = pth.replace("\\", "\\\\")                 #changes / to //. done (LIKE uses escape-characters)
    cur.execute('SELECT "path" FROM "Access"' + 
                ' WHERE "path" LIKE %(path)s', {'path':path})
    paths = cur.fetchall()
    if len(paths) != 0:
        print("Paths like " + path + " found")
        return paths
    else:
        print("Paths: " + path + " not found")
        return ""

def addLevel(level, path, con, reload):
    cur = con.cursor()
    cur.execute('INSERT INTO "Access" ("userID", "path", "access") VALUES ' + 
                "(%(id)s, %(path)s, %(rld)s)", {'id':level, 'path':path, 'rld':reload})
    try:
        con.commit()
        print("Row added")
        print("AccessDB.addRule return code: 0")
        # os.system('sudo chown root ' + path)
        # os.system('sudo chmod 700 ' + path)
        return 0
    except:
        print("Row adding failed")
        print("AccessDB.addRule return code: 1")
        return 1

def updateLevel(levelAfter, path, con, reload):
    cur = con.cursor()
    cur.execute('UPDATE "Access" SET "userID" = %(levelA)s, "access" = %(rld)s' +
                ' WHERE "path" = %(path)s',
                {'path':path, 'levelA':levelAfter, 'rld':reload})
    try:
        con.commit()
        print("Level updated")
        print("AccessDB.updateRule return code: 0")
        return 0
    except:
        print("Level update failed")
        print("AccessDB.updateRule return code: 1")
        return 1

def setLevel(level, userLevel, path, con):
    reload = 0
    if str(level) == str(userLevel):
        reload = 1
    print("path level: " + str(level) + "user level:" + str(userLevel) + "reload:" + str(reload))
    cur = con.cursor()
    cur.execute('SELECT "userID" FROM "Access"' + 
                ' WHERE "path" = %(path)s', {'path':path})
    currentLevel = cur.fetchall()
    if len(currentLevel) != 0:
        print("Level for path: " + path + " is " + str(currentLevel[0][0]))
        errorcode = updateLevel(level, path, con, reload)
    else:
        print("Rule for path: " + path + " not found")
        errorcode = addLevel(level, path, con, reload)
    print("AccessDB.setRule return code: " + str(errorcode))

def selectRuleMand(userLevel, path, con):
    cur = con.cursor()
    cur.execute('SELECT "userID", "access" FROM "Access"' + 
                ' WHERE "path" = %(path)s', {'path':path})
    pathLevel = cur.fetchall()
    
    if len(pathLevel) != 0:
        print("Level for path: " + path + " is " + str(pathLevel[0][0]))
        cur.execute('SELECT "' + str(pathLevel[0][0]) +'" FROM "Levels"' + 
                ' WHERE "LevelNum" = %(userLevel)s', 
                {'userLevel':userLevel})
        rule = cur.fetchall()
        print("Rule for path: " + path + " is " + str(rule[0][0]))
        print("Relogin expected: " + str(pathLevel[0][1]))
        return rule[0][0], pathLevel[0][1]
    else:
        print("Rule for path: " + path + " not found")
        return "rwx", "0"

def selectPathLevel(con, path):
    cur = con.cursor()
    cur.execute('SELECT "userID" FROM "Access"' + 
                ' WHERE "path" = %(path)s', {'path':path})
    level = cur.fetchall()
    if len(level) != 0:
        print("Level for path: " + path + " is " + str(level[0][0]))
        return level[0][0]
    else:
        return 0 

def closeConnection(con):
    con.close()
    print("Connection closed")


if __name__ == "__main__":
    con = connectToDB()
    pathBefore = 'C:\\Users\\tester'

    print(selectRules(0, "/Users/tester/ban", con))
    closeConnection(con)
