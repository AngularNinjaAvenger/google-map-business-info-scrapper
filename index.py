from  Get_Names import Gmap
from Get_info import  Get

Gmap = Gmap()
Get = Get()
class Index:
	def __init__(self):
		pass
	def main(self):
		print("""


			**********************
			  WELCOME \\_(*_*)_/\
			
			Enter Action:

			1.  To get names from map
			2.  To get names and get thier info
			3.  to get thier info only
		
			""")
		userChoice = input("Choice: ")
		self.initialize_choice(userChoice)
	def initialize_choice(self,choice):
		nitch = input("Enter your nitch: ")
		location = input("Enter your location: ")
		# nitch = "shoprite"
		# location = "lagos"
		file = f"maps_{nitch}_{location}_data.csv"
		info = {
		    		"nitch":nitch,
		    		"location":location
		    	}
		if choice == "1":
			Gmap.main(nitch,location)
			pass
		elif choice == "2":
		    if Gmap.main(nitch,location):
		    	
		    	Get.main(file,info)
		elif choice == "3":
			Get.main(file,info)
			pass
		else:
			pass
Index().main()