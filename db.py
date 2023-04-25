import psycopg2

def connect():
    conn = psycopg2.connect(
        #database local

        host="localhost",
        database="black-list",
        user="postgres",
        password="root"

        #db prod

        #host="35.193.50.37",
        #database="consalud-refund",
        #user="postgres",
        #password="NJhshvcvhHk3pADO"

        #TESTING
        #host= 34.69.113.26
        #database= consalud-refund
        #user = postgres
        #password = NJhshvcvhHk3pADO
       
    )
    return conn


