class Fruits: #abtract class
    def apple(self): #abstract method
        pass
    def banana(self):
        pass
class Fruitscolor(Fruits):
    def apple(self):
        print("apple color is red")    
    def banana(self):
            print("banana color is yellow")       
ob=Fruitscolor()
ob.apple()
ob.banana()
