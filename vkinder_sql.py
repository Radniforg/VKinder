import psycopg2 as pg

#

def partner_add_block(conn, id_user, block_string):
    cur = conn.cursor()
    cur.execute("SELECT * FROM block;")
    new_user = 1
    for user in cur.fetchall():
        if user[0] == id_user:
            user[1] = user[1] + ', ' + block_string
            new_user = 0
            break
    if new_user == 1:
        cur.execute("INSERT INTO block (user_id, blocked_list) VALUES (%s, %s)", (id_user, block_string))

def block_check(conn, user_id):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS block (user_id varchar(12) PRIMARY KEY, blocked_list TEXT);")
    cur.execute("SELECT * FROM block;")
    new_user = 1
    something = cur.fetchall()
    for user in something:
        if user[0] == user_id:
            new_user = 0
            block_list = user[1]
    if new_user == 1:
        block_list = ' '
    return block_list

def sql_result(conn, id_user, result):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS vinder_results (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(12),
                        results TEXT);''')
    cur.execute("INSERT INTO block (user_id, blocked_list) VALUES (%s, %s)", (id_user, result))

def restart(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE block")
    cur.execute("DROP TABLE vinder_results"
                "")

if __name__ == '__main__':
    with pg.connect(database='vkinder', user='vinder', password='vinder', host='localhost', port=5432) as conn:
        restart(conn)