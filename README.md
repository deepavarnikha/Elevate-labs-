Medical Appointment No Shows Dataset Cleaning – README

## Objective
This script performs data cleaning and preprocessing on the raw Medical Appointment No Shows dataset (`medical_appointment_no_shows.csv`) to make it analysis-ready.

## Tools Used
- **Python**
- **Pandas**

## Steps Performed

### 1. **Load Dataset**
- Reads the raw dataset from a CSV file into a Pandas DataFrame.

### 2. **Initial Inspection**
- Displays the data structure (`.info()`) and provides an overview of missing value counts using `.isnull()`.

### 3. **Remove Duplicates**
- Drops any exact duplicate records from the dataset using `.drop_duplicates()`.

### 4. **Handle Missing Values**
- Ensures no missing values remain:
  - Confirms that all columns (`PatientId`, `AppointmentID`, `Gender`, `ScheduledDay`, etc.) have no null values.
  - Handles any missing values dynamically (though this dataset initially contained none).

### 5. **Standardize Text Values**
- Standardizes the case and whitespace for relevant columns:
  - **Gender**: Converted to lowercase and stripped of unnecessary spaces.
  - **Neighbourhood**: Standardized to title case and stripped of whitespace.

### 6. **Date Format Conversion**
- Converts `ScheduledDay` and `AppointmentDay` columns:
  - Transforms these columns into consistent `dd-mm-yyyy` format using `pd.to_datetime()` and `dt.strftime()`.

### 7. **Clean Column Headers**
- Cleans and standardizes column headers:
  - Converts to lowercase.
  - Replaces spaces with underscores (e.g., `PatientId` → `patientid`).

### 8. **Check and Fix Data Types**
- Adjusts data types where necessary:
  - **Age**: Ensured to be an integer.
  - **Dates (ScheduledDay, AppointmentDay)**: Converted to datetime objects.

### 9. **Final Check**
- Prints cleaned dataset structure and confirms all missing values, duplicates, and format inconsistencies are handled.

### 10. **Save Output**
- Saves the cleaned dataset as `medical_appointment_no_shows_cleaned.csv`.


### Output
medical_appointment_no_shows_cleaned.csv** — This cleaned and processed dataset is now ready for further analysis or visualization.
