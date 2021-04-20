import os
import csv
#from tabulate import tabulate
import json
import sys

class StudentReportGenerator:

    # command to be executed
    '''
        “python main.py courses.csv students.csv tests.csv marks.csv output.json
    '''
    def __init__(self):
        
        if len(sys.argv)>6 or len(sys.argv)<6:
            print("Error in the input")
            return
            
        self.file_name = str(sys.argv[5])
        self.table = self.process_marks(str(sys.argv[4])) 
        self.students_report = self.generate_student_report(self.table)
        self.courseMap = self.courses_map(str(sys.argv[1])) 
        self.s_name = self.students_map(str(sys.argv[2])) 
        #self.display_tabularReport(self.students_report)
        self.test=self.process_tests(str(sys.argv[3])) 
        self.generate_Json(self.students_report)
    ''' method to store tests.csv in a HashMap . 
        key: id 
        value : list which has course_id, weight
    '''
    def process_tests(self, filename):
        data = {}
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["id"]] = [row["course_id"]]

                data[row["id"]].append(row["weight"])
            # print(data)
        return data
    
    ''' method to store marks.csv in a list by joining the data from given csv files with tes_id as reference 
        2D list
    '''
    def process_marks(self, marks_file):
        test_map = self.process_tests(str(sys.argv[3]))
        final_marks_data = []
        with open(marks_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                marks_data = []
                marks_data.append(row["test_id"])
                marks_data.append(row["student_id"])
                marks_data.append(row["mark"])
                marks_data.extend(test_map.get(marks_data[0]))
                final_marks_data.append(marks_data)
        # print("final",final_marks_data)
        # print(len(final_marks_data))
        return final_marks_data
    
    ''' core logic to process and store the student data in a nested HashMap.
        { student_id : { course_id: avg_course_mark}}
        This method would return a hashmap with updated values for each student in the csv file.     

    '''
    def generate_student_report(self, table):
        student = {}
        for row in table:
            try:
                #keep track of the course marks
                running_sum = 0.0
                temp = {}
                #populating the HashMap by checking the keys and updating the values accordingly.
                if(row[1] not in student):
                    student[row[1]] = temp
                    if(row[3] not in temp):
                        running_sum+=(int(row[-1]) * int(row[2])/100)
                        temp[row[3]] = running_sum
                    else:
                        temp[row[3]]+=(int(row[-1]) * int(row[2])/100)
                else:
                    course_map = student[row[1]]
                    if(row[3] not in course_map):
                        running_sum+=(int(row[-1]) * int(row[2])/100)
                        course_map[row[3]] = running_sum
                    else:
                        course_map[row[3]]+=(int(row[-1]) * int(row[2])/100)

            except:
                print("Exception occured while generating the student's report!")

        return student

    '''
    The below method used to store the courses csv in a HashMap.
    {id : [name,teacher]}
    '''    
    def courses_map(self, course_file):
        course_map = {}
        with open(course_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                course_map[row["id"]] = [row["name"]]
                course_map[row["id"]].append(row["teacher"])
            # print(course_map)
        return course_map
    
    ''' 
    The below method stores the students.csv file in a HashMap
    { id : name } 
    '''
    def students_map(self, student_file):
        student_map = {}
        with open(student_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                student_map[row["id"]] = row["name"]
            # print(student_map)
        return student_map
    
    '''
    The below method is used to calculate the average score of each course taken by the student
    returns average score.
    '''
    def calculate_average(self, student_course_map):
        local_sum = 0.0
        for k in student_course_map.keys():
            local_sum+=student_course_map[k]
        return float(local_sum)/len(student_course_map)
    '''
    The below method is used to write to the file i.e. report generation. 
    The Report is populated with each student's information in a tabular format.  
    '''
    '''
    def display_tabularReport(self, students_report):
        student_data=[]
        f=open(self.file_name,"w+")
        
        cnt=0
        for student_id in sorted(students_report.keys()):
            avg = self.calculate_average(students_report[student_id])
            if(cnt!=0):
                f.write("\n")
                f.write("\n")
            cnt+=1
            f.write("-"*44)
            f.write("\n")
            f.write("Student Id: %d" %(int(student_id)))
            f.write(", name: %s" %(self.s_name[student_id]))
            f.write("\n")
            
            c_map = students_report[student_id]
            
            for course in c_map.keys():
                details=[]
                details.append(str(self.courseMap[course][0]))
                details.append(str(self.courseMap[course][1]))
                details.append("{:.2f}".format(c_map[course]))
                student_data.append(details)
            
            f.write(tabulate(student_data,headers=["Course","Teacher's Name","Final Grade(%)"]))
            f.write("\n\n")

            student_data=[] #clear the data after writing it in the file

            f.write("Total Average: %.2f" %(avg))
            f.write("%")
            f.write("\n")
            f.write("-"*44)
            f.write("\n")
        f.close()
    '''
    '''
    The below method is used to write to the file i.e. report generation. 
    The Report is populated with each student's information in a json format.  
    '''
           
    def generate_Json(self,students_report):
           students=[]
           
           f=open(self.file_name,"w+")
           for student_id in sorted(students_report.keys()):
               studdict={}
               studdict["id"]=int(student_id)
               studdict["name"]=self.s_name[student_id]
               studdict["totalAverage"]="{:.2f}".format(self.calculate_average(students_report[student_id]))
               c_map=students_report[student_id]
               
               details=[]
               for course in c_map.keys():
                   detailsdict={}
                   detailsdict["id"]=course
                   detailsdict["name"]=str(self.courseMap[course][0])
                   detailsdict["teacher"]=str(self.courseMap[course][1])
                   detailsdict["courseAverage"]="{:.2f}".format(c_map[course])
                   details.append(detailsdict)
               studdict["Courses"]=details
               students.append(studdict)
           y=json.dumps(students)
           f.write(y)
           f.close()
            
               
'''creating the instance of the class, whose constructor will perform all the operations
   and writes it to the specified file passes as argument.
'''
report = StudentReportGenerator()

#change the argument to create a new report of your name of choice.
