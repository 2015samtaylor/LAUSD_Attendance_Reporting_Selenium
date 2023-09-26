```markdown
# LAUSD Attendance Reporting Automation

This Python script automates attendance reporting for LAUSD schools using Selenium and BeautifulSoup. It performs the following tasks:

1. Logs into the CA PowerSchool platform.
2. Selects a school from a predefined list.
3. Refreshes attendance data within a specified date range.
4. Runs attendance summary reports by grade, and parses it.
5. Downloads and parses ADA/ADM reports.
6. Saves the reports to Excel files.

## Prerequisites

- Python 3.x
- pipenv (for virtual environment management)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/lausd-attendance-reporting.git
   ```

2. Navigate to the project directory:

   ```bash
   cd lausd-attendance-reporting
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   pipenv shell
   pipenv install
   ```

## Usage

1. Start the Jupyter Notebook server within the virtual environment:

   ```bash
   jupyter notebook

   ```

2. Open the `LAUSD_Attendance_Reporting.ipynb` notebook.

3. In the first cell of the notebook, you will be prompted to enter your CA PowerSchool Username and Password. This is also the section to change the start_date, end_date and reporting month. All of these variables are necessary for accuracy:

   ```python
   import getpass

   # Prompt the user for a password
   username = (str(input('Enter your CA PowerSchool Username: ')))
   password = getpass.getpass("Enter your CA PowerSchool Password: ")
   
   start_date = '08/14/2023'
   end_date = '09/08/2023'
   month_num = '1'
   ```

   Enter your credentials when prompted.

4. Run the remaining cells in the notebook to automate the attendance reporting process.

5. The script will log in, select the school, refresh attendance data, run reports, and save them to Excel files.

6. When you're finished, shut down the Jupyter Notebook server.


For any questions or issues, please contact Sam Taylor.
```
