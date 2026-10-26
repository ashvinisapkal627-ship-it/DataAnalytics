import pandas as pd

#function to calculate average
def calculate_average(marks):
    return sum(marks) / len(marks)

#user input
n=int(input("Enter the number of students: "))
names=[]
marks=[]

for i in range(n):
    name=input("enter the name of the student: ")
    mark=float(input("enter the marks of the student:"))
    names.append(name)
    marks.append(mark)

#create dataset
df=pd.DataFrame({
    "name": names,
    "marks": marks
})

#conditional statements
def result(mark):
    if mark>=75:
        return "distinction"
    elif mark>=50:
        return "pass"
    else:
        return "fail"

df["result"]=df["marks"].apply(result)

#display dataset
print("\ndataset:")
print(df)

#loop for processing values
print("\nstudent analysis:")
for mark in marks:
    if mark >= 75:
        print(mark,"distinction")
    elif mark>=50:
        print(mark,"pass")
    else:
        print(mark,"fail")

#analysis
print("\naverage marks:", calculate_average(marks))
print("highest marks:", max(marks))
print("lowest marks:", min(marks))
