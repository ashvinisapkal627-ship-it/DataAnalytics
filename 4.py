import pandas as pd

while True:
    try:
        n = int(input("Enter the number of students: "))
        if n > 0:
            break
        print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a whole number.")

names=[]
ages=[]
departments=[]
dates=[]

for i in range(n):
    print("\nenter the details of student",i+1)
    name=input("enter the name of the student: ")

    while True:
        try:
            age = int(input("enter the age of the student: "))
            break
        except ValueError:
            print("Invalid age. Please enter a whole number.")

    department=input("enter the department of the student: ")
    date=input("enter the addmission date (YYYY-MM-DD): ")
    names.append(name)
    ages.append(age)
    departments.append(department)
    dates.append(date)

    #create dataframe
    date={
        'name': names,
        'age': ages,
        'department': departments,
        'admission_date': dates

    }

    df=pd.DataFrame(date)
    print("\noriginal data:")
    print(df)
    print("\noriginal data types:")
    print(df.dtypes)


    #1.data type conveersion
df['age']=df['age'].astype('int')

#2.string manuplation
df['name']=df['name'].str.strip()

df['name']=df['name'].str.title()

df['department']=df['department'].str.upper()

#3. date type conversion
df['admission_date']=pd.to_datetime(df['admission_date'],
                                    format='%Y-%m-%d')

df['year']=df['admission_date'].dt.year

df['month']=df['admission_date'].dt.month

df['day']=df['admission_date'].dt.day


#Display  transformed data
print("\ntransformed data:")
print(df)
print("\ntransformed data types:")
print(df.dtypes)

