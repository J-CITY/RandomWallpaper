import sqlite3
import os

class Database:
	def __init__(self):
		self.dbName = 'lib.db'
		self.tableName = 'tags'
		self.create()

	def create(self):
		self.conn = sqlite3.connect(self.dbName)
		self.cursor = self.conn.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS """ + self.tableName + """ 
		(tag TEXT,
		val INTEGER)
		""")
		
	def insert_and_get(self, tag, val):
		self.cursor.execute('SELECT * FROM '+ self.tableName + ' WHERE (tag=?)', (tag,))
		entry = self.cursor.fetchone()
		if entry is None:
			print('No tag found')
			self.cursor.execute('INSERT INTO '+ self.tableName + ' (tag, val) VALUES (?,?)', (tag, val))
			self.conn.commit()
			self.cursor.execute('SELECT * FROM '+ self.tableName + ' WHERE (tag=?)', (tag,))
			return self.cursor.fetchone()
		else:
			return entry
	
	def select_tag(self, tag):
		self.cursor.execute('SELECT * FROM '+ self.tableName + ' WHERE (tag=?)', (tag,))
		return self.cursor.fetchone()
		
	def update_tag(self, tag, val):
		self.cursor.execute('UPDATE ' + self.tableName + ' SET val=? WHERE tag=?', (val, tag))
		self.conn.commit()
	
	def execute(self, text, params=()):
		self.cursor.execute(text, params)
		return self.cursor.fetchall()
		
	def print_db(self):
		self.cursor.execute('SELECT * FROM '+ self.tableName)
		table = self.cursor.fetchall()
		
		for t in table:
			print(t)