class Demo:
    class_var=[]

    def __init__(self,name):
        self.name = name
        self.instance_var = []

a = Demo("Ameet") #created a object whose name is a 
b = Demo("Shravanee") # created a object whose name is b

a.class_var.append("Added for object a")
b.class_var.append("added for object b")

a.instance_var.append("added instance var for a") 
b.instance_var.append("added instance var for b")

print("a.class_var", a.class_var) #added for object a and added for object b
print("b.class_var", b.class_var) # added or object a and added for object b

print('a.instance_var', a.instance_var) #added instance var for a

print('b.instance_var', b.instance_var) #added instance var for b