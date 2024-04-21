"""
Singleton is a creational design pattern, which ensures 
that only one object of its kind exists and provides a 
single point of access to it for any other code.
"""

class Singleton:
    """
		Singleton pattern.
		Overload class that must have one instance.
		Stores the instance in a static variable: Class.instance
	"""
	
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Singleton, cls).__new__(cls)
		return cls.instance