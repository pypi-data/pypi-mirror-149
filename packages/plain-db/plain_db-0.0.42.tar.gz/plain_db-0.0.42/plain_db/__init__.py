#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'plain_db'
import os

def getFile(fn, isIntValue=True):
	result = {}
	if not os.path.exists(fn):
		return result
	with open(fn) as f:
		for line in f.readlines():
			line = line.strip()
			if not line:
				continue
			if isIntValue:
				key = ' '.join(line.split()[:-1])
				value = int(line.split()[-1])
			else:
				key = line.split()[0]
				value = ' '.join(line.split()[1:])
			result[key] = value
	return result

class DB(object):
	def __init__(self, name, isIntValue=True, default = None): 
		self.fn = 'db/' + name
		self.isIntValue = isIntValue
		self.items = getFile(self.fn, isIntValue=isIntValue)
		self.defaultValue = default

	def update(self, key, value):
		key = str(key)
		if key not in self.items:
			self.items[key] = value
			self.appendSave(key, value)
			return
		self.items[key] = value
		self.save()

	def remove(self, key):
		key = str(key)
		if key in self.items:
			del self.items[key]
			self.save()
			return True
		return False

	def inc(self, key, value):
		key = str(key)
		oldValue = self.items.get(key, 0)
		self.update(key, oldValue + value)

	def get(self, key, default=None):
		key = str(key)
		if key in self.items:
			return self.items[key]
		if default != None:
			return default
		return self.defaultValue

	def appendSave(self, key, value):
		key = str(key)
		if len(self.items) == 1:
			os.system('mkdir db > /dev/null 2>&1')
			with open(self.fn, 'w') as f:
				f.write(key + ' ' + str(value))
			return
		with open(self.fn, 'a') as f:
			f.write('\n' + key + ' ' + str(value))

	def save(self):
		lines = [key + ' ' + str(self.items[key]) for key in self.items]
		lines.sort()
		towrite = '\n'.join(lines)
		os.system('mkdir db > /dev/null 2>&1')
		with open(self.fn + 'tmp', 'w') as f:
			f.write(towrite)
		os.system('mv %stmp %s' % (self.fn, self.fn))

def load(fn, isIntValue=True):
	return DB(fn, isIntValue=isIntValue)

class NoValueDB(object):
	def __init__(self, name):
		self._db = DB(name)

	def add(self, key):
		if self._db.get(key, 0) >= 1:
			return False
		self._db.update(key, 1)
		return True

	def remove(self, key):
		return self._db.remove(key)

	def toggle(self, key):
		if self._db.get(key):
			self.remove(key)
			return False
		self.add(key)
		return True

	def contain(self, key):
		return self._db.get(key)

	def items(self):
		return list(self._db.items.keys())

def loadKeyOnlyDB(fn):
	return NoValueDB(fn)

class LargeDB(object):
	def __init__(self, name, isIntValue=False, 
			default=None):
		self.name = name
		self._db = DB(name, isIntValue=isIntValue, 
			default = default)

	def load(self):
		self._db.load()

	def get(self, key, default=None):
		key = str(key)
		return self._db.get(key, default)

	def update(self, key, value):
		key = str(key)
		if self._db.get(key) == value:
			return
		self._db.items[key] = value
		self._db.appendSave(key, value)

	def items(self):
		return list(self._db.items.items())

	def keys(self):
		for key, value in self.items():
			if value:
				yield key

	def getFn(self):
		return self._db.fn

	def save_dont_call_in_prod(self):
		f2 = loadLargeDB(self.name + 'tmp')
		for key, value in self.items():
			f2.update(key, value)
		os.system('mv %s %s' % (f2.getFn(), self.getFn()))

def loadLargeDB(fn, isIntValue=False, default=None):
	return LargeDB(fn, isIntValue=isIntValue, default = default)

def cleanupLargeDB(fn):
	f1 = loadLargeDB(fn)
	f2 = loadLargeDB(fn + 'tmp')
	for key, value in f1.items():
		f2.update(key, value)
	os.system('mv %s %s' % (f2.getFn(), f1.getFn()))