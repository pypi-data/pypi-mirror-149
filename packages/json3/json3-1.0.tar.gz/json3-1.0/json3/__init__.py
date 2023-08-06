class Json(object):
	def __init__(self, json):
		for key in json:
			if type(json[key]) == type(json):
				json[key] = Json(json[key])
		self.__dict__ = json
		self.json = json
	def __getitem__(self, key):
		return self.json[key]
	def __setitem__(self, key, value):
		self.json[key] = value
	def __delitem__(self, key):
		del self.json[key]
	def call(self, json):
		return Json(json)
	def __str__(self):
		return str(self.json)
	def __repr__(self):
		return self.__str__()
	__docs__ = """
	 class Json(object)
	 Beautiful Simple Json Storage
	"""
	def __add__(self, other):
		raise NotImplementedError(str(other))
	def __enter__(self):
		return self
if __name__ == "__main__":
   print(Json({"hello": "dhxh","r": {"wering": "jdjd"}}))
