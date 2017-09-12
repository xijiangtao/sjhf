#coding=utf-8

import sqlite3
import asyncio


conn = sqlite3.connect('frame.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS frames(offset number, frame_no varchar(20))')


async def insert(offset, number):
	in_state = 'INSERT INTO frames VALUES (%d, %s)' % (offset, number)
	cursor.execute(in_state)
