# Biometric Student Attendance & Performance Monitoring System

An **ESP32-based biometric attendance and academic performance monitoring project** combining a fingerprint-sensor hardware component with a Python and Streamlit dashboard for students, teachers, and administrators.

> **Project status:** Academic prototype. The dashboard includes working sample-data visualizations and CSV upload interfaces. The provided fingerprint Python script is an incomplete prototype; an end-to-end ESP32-to-dashboard attendance pipeline is **not demonstrated** in the supplied source files.

## Project Overview

The project explores a more structured way to manage student attendance and review academic performance. Its intended workflow is to identify a student using a fingerprint sensor connected to an ESP32, record entry/exit events, and present attendance and performance information through role-based dashboards.

The provided Streamlit application demonstrates student management, attendance and punctuality visualization, CGPA trends, class-test charts, and CSV-based data uploads. Several charts currently use generated or hardcoded demonstration data rather than live fingerprint records.

## Objectives

- Explore fingerprint-based student identification and entry/exit tracking.
- Provide separate interfaces for **Admin**, **Teacher**, and **Student** roles.
- Organize student information, attendance data, and class-test marks.
- Visualize CGPA, attendance, punctuality, and assessment performance.
- Support CSV uploads for basic academic record management.
- Establish a foundation for future ESP32-to-dashboard integration.

## Hardware and Software

| Category | Component | Purpose |
| --- | --- | --- |
| Hardware | **ESP32 microcontroller board** | Controller used in the hardware project |
| Hardware | **Fingerprint sensor** | Biometric identification component |
| Language | **Python** | Application and fingerprint prototype logic |
| Web UI | **Streamlit** | Role-based dashboard |
| Data processing | **Pandas** | Reading, filtering, and merging tabular data |
| Visualization | **Plotly Express** | Interactive charts |
| Data format | **CSV** | Student and marks datasets |
| Prototype library | **PyFingerprint** | Referenced in commented-out sensor code; hardware compatibility/integration not verified |

*The exact ESP32 variant, fingerprint sensor model, wiring, firmware, and communication protocol are not specified in the provided files.*

## System Architecture (Intended)

```text
Student Fingerprint
       |
       v
Fingerprint Sensor
       |
       v
ESP32 Microcontroller
       |
       v
Attendance Event / Data Transfer  [integration pending]
       |
       v
Python Data Processing
       |
       v
Streamlit Web Dashboard
       |
       +--> Admin: Student Management
       +--> Teacher: Attendance & Marks Analysis
       +--> Student: Performance Visualization
```

**Important:** This is the intended architecture, not a verified end-to-end data flow in the uploaded code. The current dashboard reads sample data and separately uploaded CSV files.

## Dashboard Features

### Admin Dashboard

- Upload a student CSV file and preview its contents.
- Add a student with name, department, student ID, and CGPA to the current session.
- Search for a student by ID in the default sample dataset.

### Student Dashboard

- **CGPA Progression:** Line chart across four example trimesters.
- **Attendance Overview:** Pie chart of attended versus missed classes, based on sample attendance percentages.
- **Punctuality Overview:** Bar chart for 24 simulated classes.
- **Class Test Performance:** Bar chart with example CT scores.
- **Course Selection:** Basic selection UI with three placeholder course names.

### Teacher Dashboard

- Select a section: **BA**, **BB**, or **BC**.
- View grouped comparisons of CGPA, attendance, and punctuality from sample records.
- Upload class-test marks CSV files and visualize marks and grade categories.
- Upload an attendance CSV file and preview the records.
- View a demonstration attendance/punctuality score report.

## Fingerprint Module

The `fingerprint.py` file sketches the following intended process:

1. Read and identify a fingerprint.
2. Match a fingerprint ID to a stored name.
3. Record a timestamped **entry** event on the first scan.
4. Record an **exit** event on a subsequent scan.
5. Print an event containing fingerprint ID, name, date, time, and action.

**Current implementation notes:** Sensor initialization, fingerprint matching, and entry/exit logic are commented out. The time function references an undefined exception variable, and the script does not persist attendance events or send them to Streamlit. It needs further implementation and testing before it can serve as a working biometric attendance recorder.

## Included Files

```text
Biometric-Student-Attendance-System/
|-- app(5).py          # Streamlit dashboard (uploaded filename)
|-- fingerprint.py     # Fingerprint attendance prototype
|-- stu_75.csv         # Student/CGPA/fingerprint-ID sample data
|-- mark_stu.csv       # Student marks sample data
|-- README.md          # Project documentation
```

The filenames above reflect the supplied files. You can rename `app(5).py` to `app.py` for convenience, but then update the launch command accordingly.

## Datasets

### `stu_75.csv`

Contains **75 student records** with these columns:

- `Student Name`
- `Student ID`
- `CGPA trimester 1`
- `CGPA trimester 2`
- `CGPA trimester 3`
- `CGPA trimester 4`
- `Fingerprint ID`

### `mark_stu.csv`

Contains **30 records** with the columns:

- `student_id`
- `marks`

**Data integration note:** The CSV files and the app's built-in sample data use different student-ID formats. The dashboard does not automatically join these uploaded datasets into a unified attendance database.

## Installation and Running the Dashboard

### Prerequisites

- Python 3.9 or newer (suggested)
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Biometric-Student-Attendance-System.git
cd Biometric-Student-Attendance-System
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install the dashboard dependencies

```bash
pip install streamlit pandas plotly
```

### 3. Start the Streamlit app

```bash
streamlit run "app(5).py"
```

Streamlit will provide a local URL for the dashboard. This runs the **dashboard demonstration**, not a fully connected fingerprint hardware system.

### 4. Explore the dashboard

Select a role in the sidebar. The current prototype uses hardcoded demonstration credentials in the Python source. **Do not deploy these credentials as a production authentication system.**

## Data Visualizations

| Chart | Purpose | Current data source |
| --- | --- | --- |
| CGPA line chart | Show example trimester progression | Hardcoded example values |
| Attendance pie chart | Show attended/missed percentage | Generated student sample data |
| Punctuality bar chart | Compare 24 classes | Randomly simulated times and percentages |
| Class-test bar chart | Compare example test scores | Hardcoded example values |
| Teacher grouped bar chart | Compare section performance | Generated student and attendance data |
| Marks distribution bar/pie charts | Review uploaded marks and grade bands | Teacher-uploaded CSV |

## Current Limitations

- The uploaded code does **not** demonstrate a working ESP32-to-Streamlit connection.
- Fingerprint acquisition and entry/exit recording are not active in `fingerprint.py`.
- No persistent database is configured; much of the data is temporary or simulated.
- Student and teacher dashboards are not fully synchronized with uploaded attendance records.
- The student CGPA and class-test charts use fixed example values.
- Login credentials are hardcoded, so authentication is **not production-secure**.
- CSV student identifiers need normalization before datasets can be reliably merged.
- The attendance report is a demonstration score table, not an exported biometric report.

## Future Improvements

- Complete and test the ESP32 firmware and fingerprint sensor integration.
- Implement a documented ESP32-to-Python communication method.
- Store attendance events in a persistent database.
- Calculate real attendance percentages and punctuality from recorded timestamps.
- Unify student IDs across uploaded datasets and dashboards.
- Add secure authentication, role permissions, and password management.
- Add report exports, validation, and error handling.
- Add deployment instructions and hardware wiring diagrams after verification.

## Academic Context

This project demonstrates an approach to combining **embedded hardware, biometric identification, Python-based data processing, and interactive educational dashboards**. It is presented as an academic prototype and a foundation for further development.

## License

No license has been specified. Add a `LICENSE` file if you want to define how others may use or redistribute this project.
