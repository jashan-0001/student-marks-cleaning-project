from pathlib import Path

import pandas as pd

# ----------------------------------
# Load Dataset
# ----------------------------------

base_dir = Path(__file__).resolve().parent
input_path = base_dir / "students_marksss.csv"
output_path = base_dir / "cleaned_students.csv"

df = pd.read_csv(input_path)

print("Original Shape:", df.shape)

# ----------------------------------
# Remove Duplicate Rows
# ----------------------------------

df = df.drop_duplicates()

# ----------------------------------
# Remove Extra Spaces
# ----------------------------------

df.columns = df.columns.str.strip()

text_columns = ["Student", "Class"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# ----------------------------------
# Convert Marks to Numeric
# ----------------------------------

numeric_columns = [
    "Maths",
    "Science",
    "English",
    "Attendance"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ----------------------------------
# Fill Missing Numeric Values
# ----------------------------------

for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

# ----------------------------------
# Remove Impossible Marks
# ----------------------------------

for col in ["Maths", "Science", "English"]:
    df = df[(df[col] >= 0) & (df[col] <= 100)]

# Attendance should also be between 0 and 100

df = df[(df["Attendance"] >= 0) & (df["Attendance"] <= 100)]

# ----------------------------------
# Reset Index
# ----------------------------------

df.reset_index(drop=True, inplace=True)

# ----------------------------------
# Save Clean Dataset
# ----------------------------------

df.to_csv(output_path, index=False)

print("\nCleaning Completed Successfully!")
print("Final Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Rows:")
print(df.head())