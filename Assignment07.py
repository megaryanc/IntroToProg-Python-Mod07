# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   <Ryan Choi>,<11/27/24>,<Assignment07>
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

class Person:
    """
       A class representing person data.

       Properties:
           first_name (str): The student's first name.
           last_name (str): The student's last name.

       ChangeLog:
           - Ryan Choi, 11.27.2024: Created the class.
       """
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self)->str:
        return self._first_name.title()

    @first_name.setter
    def first_name(self, value: str) -> None:
        if value.isalpha():
            self._first_name = value
        else:
            raise ValueError("First name must be alphabetic")

    @property
    def last_name(self) -> str:
        return self._last_name.title()

    @last_name.setter
    def last_name(self, value: str) -> None:
        if value.isalpha():
            self._last_name = value
        else:
            raise ValueError("Last name must be alphabetic")

    def __str__(self) -> str:
        return f'{self.first_name},{self.last_name}'

class Student(Person): # Inherit from Person
    """
        A class representing student data.

        Properties:
        - first_name (str): The student's first name.
        - last_name (str): The student's last name.
        - course_name(str): The course name that the student registered in.

        ChangeLog:
        Ryan Choi,11.27.2024, Created the class.
        """
    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        return self._course_name

    @course_name.setter
    def course_name(self,value) -> None:
        self._course_name  = value

    def __str__(self) -> str:
        return f'{super().__str__()},{self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list) :
        """ This function reads data from a json file and loads it into a list of dictionary rows

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :param file_name: string data with name of file to read from
        :param student_data: list of dictionary rows to be filled with file data

        :return: list
        """

        try:
            file = open(file_name, "r")
            list_of_dictionary_data = json.load(file)
            for student in list_of_dictionary_data:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of dictionary rows

        ChangeLog: (Who, When, What)
        Ryan Choi,11.27.2024,Created function

        :param file_name: string data with name of file to write to
        :param student_data: list of dictionary rows to be writen to the file

        :return: None
        """
        try:
            list_of_dictionary_data: list = []
            for student in student_data: # Convert list of student objects to dictionary rows for JSON file
                enrollments_json: dict = {"FirstName": student.first_name,
                                      "LastName": student.last_name,
                                      "CourseName": student.course_name}
                list_of_dictionary_data.append(enrollments_json)

            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            IO.output_error_messages(message=message,error=e)
        finally:
            if file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    Ryan Choi,11.27.2024,Created Class
    Ryan Choi,11.27.2024,Added menu output and input functions
    Ryan Choi,11.27.2024,Added a function to display the data
    Ryan Choi,11.27.2024,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the a custom error messages to the user

        ChangeLog: (Who, When, What)
        Ryan Choi,11.27.2024,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        Ryan Choi,11.27.2024,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice(menu: str) -> str:
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        Ryan Choi,11.27.2024,Created function

        :return: string with the users choice
        """
        menu_choice = input('What would you like to do: ')
        while menu_choice not in ['1', '2', '3', '4']:
            IO.output_error_messages('Please enter a number between 1 and 4.')
            menu_choice = input("What would you like to do: ")
        return menu_choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        Ryan Choi,11.27.2024,Created function

        :param student_data: list of dictionary rows to be displayed

        :return: None
        """

        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)
    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name, last name, and course name from the user """

        try:
            first_name = input("Enter the student's first name: ")
            last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")

            # Create the Student object
            student = Student(first_name=first_name, last_name=last_name, course_name=course_name)

            # Add the Student object to the list
            student_data.append(student)
            print(f"\nYou have registered {student.first_name} {student.last_name} for {student.course_name}.")

        except ValueError as e:
            IO.output_error_messages(message="Input validation failed! Please enter valid alphabetic names.", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    print(MENU)
    menu_choice = IO.input_menu_choice(menu= MENU)

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(student_data=students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
