from flask import Flask, request, Response
import json
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
    
@app.route('/', methods=['GET', 'POST'])
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

def get_user_post():
    if (request.method == 'GET'):
        get_post = request.args.get('content')
        resp = {
            "userPost" : get_post
        }
        print()
        return Response(json.dumps(resp),
                        mimetype="application/json",
                        status=200)


