# import libraries modules and other code base files

#calculate function
def calculate(gwa):
    return gwa

# user interface container
class interface_MainUi:

    # contructor for main ui: initializes instance attributes
    def __init__(self):
        self.self = self
   
   # feature handling
    def main_menu(self):
        print("""
            
            Grade Management System

            Options: 
            1. Students        

""")
        user_choice = int(input("What's on your mind?: "))
        
        if user_choice == 1:
            interface_student = interface_MainUi.interface_StudentUi("Carl, ")
            print(interface_student.student_menu())
        else:
            return 0

    # subclass student interface
    class interface_StudentUi:

     # constructor for student ui: initializes instance attributes
        def __init__(self, menu_student):
            self.menu_student = menu_student

    # feature handling
        def student_menu(self):
            return f"{self.menu_student} this is a user interface for student ui"

# starter
if interface_MainUi().main_menu() == 0:
    print("No correct values have found...")

