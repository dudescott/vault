import sqlite3 as sql
import pyperclip
import os

def insert(c, site, username, password, note):
    sites = get_sites(c)
    if site in [s[0] for s in sites]:
        c.execute('update pwm set username = ?, password = ?, note = ? where site = ?',(username, password, note,site))
    else:
        c.execute('insert into pwm values(?,?,?, ?)',(site, username, password, note))

def delete(c, site):
    c.execute('delete from pwm where site == ?', (site,))

def retrieve(c, site):
    c.execute('select * from pwm where site == ?', (site,))
    cred = c.fetchall()
    if cred != []:
        pyperclip.copy(cred[0][2])
    return cred

def get_sites(c):
    try:
        c.execute('select site from pwm order by site desc')
        return c.fetchall()
    except sql.OperationalError:
        return []
    

def pwm(action, site, username, password, note):
    if not os.path.exists('pwm.db.vsa') and not os.path.exists('pwm.db'):
        conn = sql.connect('pwm.db')
        c = conn.cursor()
        c.execute("""
            create table pwm (
                site char(100), 
                username char(100),
                password char(20), 
                note char(500)
                )
            """)
        conn.commit()
        conn.close()
    if os.path.exists('pwm.db'):
        conn = sql.connect('pwm.db')
        c = conn.cursor()
        if action.lower() == 'i': # insert
            insert(c, site, username, password, note)
        elif action.lower() == 'd': # delete
            delete(c, site)
        elif action.lower() == 'r': # retrieve
            return retrieve(c, site)
        elif action.lower() == 'l': # list
            return get_sites(c)
        conn.commit()
        conn.close()
 
