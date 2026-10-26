
import pandas as pd



def get_dataframe(df_name, columns):
    """
    Collect data from the user and create a DataFrame.
    columns: list of column names for the dataset.
    """
    print(f"\n--- Enter data for {df_name} ---")
    print(f"Columns: {columns}")

    while True:
        try:
            num_rows = int(input(f"How many rows for {df_name}? "))
            if num_rows < 0:
                print("Please enter zero or a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    data = {col: [] for col in columns}

    for r in range(num_rows):
        print(f"\nRow {r + 1}:")

        for col in columns:
            value = input(f"  {col}: ").strip()

            # Convert numeric input to int or float
            try:
                if value == "":
                    pass
                elif value.isdigit():
                    value = int(value)
                else:
                    value = float(value)
            except ValueError:
                pass  # Keep non-numeric input as a string

            data[col].append(value)

    df = pd.DataFrame(data)

    print(f"\n{df_name}:")
    print(df)
    print()

    return df



# STEP 1: Dataset 1 - Student basic information

print("=" * 60)
print("STEP 1: Build Dataset 1 - Student Basic Information")
print("=" * 60)

students_df1 = get_dataframe(
    "Dataset 1 (Students)",
    ["StudentID", "Name", "Branch"]
)



# STEP 2: Dataset 2 - Student marks

print("=" * 60)
print("STEP 2: Build Dataset 2 - Student Marks")
print("=" * 60)

marks_df2 = get_dataframe(
    "Dataset 2 (Marks)",
    ["StudentID", "Marks"]
)



# STEP 3: Dataset 3 - New batch of students
# 
print("=" * 60)
print("STEP 3: Build Dataset 3 - New Students")
print("=" * 60)

students_df3 = get_dataframe(
    "Dataset 3 (New Students)",
    ["StudentID", "Name", "Branch"]
)



# 3A. Vertical concatenation (axis=0)

combined_students = pd.concat(
    [students_df1, students_df3],
    axis=0,
    ignore_index=True
)

print("\nVertical Concatenation (axis=0):")
print(combined_students)



# 3B. Horizontal concatenation (axis=1)

print("\n--- Enter Attendance Data ---")

n_rows_extra = len(students_df1)
print(f"Enter attendance for {n_rows_extra} rows.")

attendance_values = []

for r in range(n_rows_extra):
    while True:
        try:
            val = float(input(f"Attendance (%) for row {r + 1}: "))
            if not 0 <= val <= 100:
                print("Enter a percentage between 0 and 100.")
                continue
            attendance_values.append(val)
            break
        except ValueError:
            print("Invalid input. Enter a number.")

extra_info = pd.DataFrame({
    "Attendance(%)": attendance_values
})

horizontal_concat = pd.concat(
    [students_df1, extra_info],
    axis=1
)

print("\nHorizontal Concatenation (axis=1):")
print(horizontal_concat)


# 
# 3C. Inner merge
# 
inner_merge = pd.merge(
    students_df1,
    marks_df2,
    on="StudentID",
    how="inner"
)

print("\nInner Merge:")
print(inner_merge)


# 
# 3D. Left merge
# 
left_merge = pd.merge(
    students_df1,
    marks_df2,
    on="StudentID",
    how="left"
)

print("\nLeft Merge:")
print(left_merge)


# 
# 3E. Right merge
# 
right_merge = pd.merge(
    students_df1,
    marks_df2,
    on="StudentID",
    how="right"
)

print("\nRight Merge:")
print(right_merge)


# 
# 3F. Outer merge
# 
outer_merge = pd.merge(
    students_df1,
    marks_df2,
    on="StudentID",
    how="outer"
)

print("\nOuter Merge:")
print(outer_merge)


# 
# 3G. Join using StudentID as the index
# 
df_a = students_df1.set_index("StudentID")
df_b = marks_df2.set_index("StudentID")

joined_df = df_a.join(
    df_b,
    how="inner"
)

print("\nJoin (index-based, inner):")
print(joined_df)


# 
# 3H. Outer join
# 
joined_outer_df = df_a.join(
    df_b,
    how="outer"
)

print("\nJoin (index-based, outer):")
print(joined_outer_df)


# 
# 3I. Merge using different column names
# 
marks_df_renamed = marks_df2.rename(
    columns={"StudentID": "ID"}
)

merge_diff_cols = pd.merge(
    students_df1,
    marks_df_renamed,
    left_on="StudentID",
    right_on="ID",
    how="inner"
).drop(columns=["ID"])

print("\nMerge with Different Column Names:")
print(merge_diff_cols)


# 
# STEP 4: Dataset X - Subjects per semester
# 
print("\n" + "=" * 60)
print("STEP 4: Build Dataset X - Subjects")
print("=" * 60)

df_x = get_dataframe(
    "Dataset X (Subjects)",
    ["StudentID", "Semester", "Subject"]
)


# 
# STEP 5: Dataset Y - Grades per semester
# 
print("=" * 60)
print("STEP 5: Build Dataset Y - Grades")
print("=" * 60)

df_y = get_dataframe(
    "Dataset Y (Grades)",
    ["StudentID", "Semester", "Grade"]
)


# 
# Merge using multiple keys
# 
merge_multi_key = pd.merge(
    df_x,
    df_y,
    on=["StudentID", "Semester"],
    how="inner"
)

print("\nMerge on Multiple Keys:")
print(merge_multi_key)


# 
# PROGRAM COMPLETED
# 
print("\n" + "=" * 60)
print("All operations completed successfully!")
print("=" * 60)
