class BMI:
	def __init__(self, age, weight, height, gender):
		self.age = age
		self.weight = weight
		self.height = height
		self. gender = gender
		self.bmi = 0

	def bmi(self):
		if self.gender.upper() == 'male'.upper():
			self.bmi = self.weight / ((self.height/100)**2) * 0.98
		else:
			self.bmi = self.weight / ((self.height/100)**2) * 0.94
		return self.bmi

	def conclusion(self):
		if self.bmi < 18.5:
			return 'underweight'
		elif self.bmi < 24.9:
			return 'normal'
		elif self.bmi < 29.9:
			return 'overweight'

