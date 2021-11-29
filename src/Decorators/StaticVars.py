def staticVars(**kwargs):
	def decorator(fn):
		for name in kwargs:
			setattr(fn, name, kwargs[name])
		return fn
	return decorator