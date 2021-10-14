from flask import Flask, request, Response
import json

from flask.wrappers import Response
import dbcreds
import mariadb

app = Flask(__name__)

def connection():
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(
                                user=dbcreds.user,
                                password=dbcreds.password,
                                host=dbcreds.host,
                                port=dbcreds.port,
                                database=dbcreds.database)
        cursor = conn.cursor()

    except:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.close()
        else:
            return ('Connection failed')
    
    return (conn,cursor)

@app.route('/')
def index():
    return ("Hello")

    
@app.route('/api/blog', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def create_post():
    if (request.method == 'POST'):
        conn = None
        cursor = None
        username = request.json.get('username')
        content = request.json.get('content')

        try:
            (conn, cursor) = connection()
            cursor.execute("INSERT INTO blog(username, content) VALUES(?,?), [username, content]")
            conn.commit()
            resp = {
                "username" : username,
                "content" : content
            }
            return Response(json.dumps(resp),
                            mimetype="application/json",
                            status=200)
        
        except mariadb.ConnectionError:
            print("Something wrong with your connection")
        except mariadb.DataError:
            print("Something wrong with your data")
        except mariadb.OperationalError:
            print("Operational error on the connection")
        except mariadb.ProgrammingError:
            print("Your query was wrong")
        except mariadb.IntegrityError:
            print("Your query would have broken the database and we stopped it")
        except:
            print("Something went wrong")

        finally:
            if (cursor != None):
                cursor.close()

            if (conn != None):
                conn.rollback()
                conn.close()
    else:
        return("Post unsuccessful")

def getUserPost():
    if (request.method == 'GET'):
        conn = None
        cursor = None
        id = request.args.get('id')

        try:
            (conn, cursor) = connection()
            if id:
                cursor.execute("SELECT * FROM blog WHERE id=?", [id,])
                result = cursor.fetchall()
                return Response(json.dumps(result, defeault=str),
                                mimetype="application/json",
                                status=200)
            else:
                return("User post not found")

        except mariadb.DataError:
            print("Something wrong with your data")
        except mariadb.OperationalError:
            print("Operational error on the connection")
        except mariadb.ProgrammingError:
            print("Your query was wrong")
        except mariadb.IntegrityError:
            print("Your query would have broken the database and we stopped it")
        except:
            print("Something went wrong")

        finally:
            if (cursor != None):
                cursor.close()

            if (conn != None):
                conn.rollback()
                conn.close()
    return(result)

def editPost():
    if (request.method == 'PATCH'):
        conn = None
        cursor = None 
        updateContent = request.json.get('content')

        try:
            (conn, cursor) = connection()
            cursor.eecute("UPDATE blog SET content=? WHERE id=?", [id, updateContent])
            conn.commit()
            resp = {
                "newContent" : updateContent
            }
            return Response(json.dumps(resp),
                            mimetype="applications/json",
                            status=200)
        except mariadb.DataError:
            print("Something wrong with your data")
        except mariadb.OperationalError:
            print("Operational error on the connection")
        except mariadb.ProgrammingError:
            print("Your query was wrong")
        except mariadb.IntegrityError:
            print("Your query would have broken the database and we stopped it")
        except:
            print("Something went wrong")

        finally:
            if (cursor != None):
                cursor.close()

            if (conn != None):
                conn.rollback()
                conn.close()  
    return(resp)

def deletePost():
    if (request.method == 'DELETE'):
        conn = None
        cursor = None 
        id = request.json.get('id')

        try:
            (conn, cursor) = connection()
            cursor.execute("DELETE FROM blog WHERE id=?", [id,])
            conn.commit()
            return Response("Post deleted",
                            mimetype="text/plain",
                            status=200)
        except mariadb.DataError:
            print("Something wrong with your data")
        except mariadb.OperationalError:
            print("Operational error on the connection")
        except mariadb.ProgrammingError:
            print("Your query was wrong")
        except mariadb.IntegrityError:
            print("Your query would have broken the database and we stopped it")
        except:
            print("Something went wrong")

        finally:
            if (cursor != None):
                cursor.close()

            if (conn != None):
                conn.rollback()
                conn.close()  
    return("Deleted")
