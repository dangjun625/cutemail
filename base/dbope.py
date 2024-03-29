# coding: utf-8
import os, sys, sqlite3
import rwlock

dblock = rwlock.RWLock()

class DBOpe:
    def __init__(self, dbpath, mode='r'):
        self.conn = None
        self.path = dbpath
        self.mode = mode
        
        self.lockid = dblock.acquire(mode)
        
        self.open()


    def open(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.path)

    def close(self):
        self.conn.close()
        self.conn = None
        dblock.release(self.lockid, self.mode)

    def execute(self, sql, iscommit=True):
        self.conn.execute(sql)
        if iscommit:
            self.conn.commit()

    def execute_param(self, sql, param, iscommit=True):
        self.conn.execute(sql, param)
        if iscommit:
            self.conn.commit()

    def query(self, sql, iszip=True):
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        
        ret = []
        if res and iszip:
            des = cur.description
            names = [x[0] for x in des]

            for line in res:
                ret.append(dict(zip(names, line)))
        else:
            ret = res
        
        cur.close()
        return ret

def openuser(cf, username, mode='r'):
    dbpath = os.path.join(cf.datadir, username, 'mailinfo.db')
    
    return DBOpe(dbpath, mode) 
    
    
