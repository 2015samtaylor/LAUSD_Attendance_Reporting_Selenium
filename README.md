---

# LAUSD Attendance Reporting Automation

This Python script automates attendance reporting for a list of schools within the Los Angeles Unified School District (LAUSD). It leverages web scraping and Selenium to interact with the LAUSD attendance reporting platform and retrieve relevant data.

The reason for this script is to download ADA ADM by Student reports, and Attendance Summary Reports for all schools. 

The final product will output reports to the all_reports folder in the naming convention of 'all_ada_adm_reports_{month_number}', and 'all_attendance_summary_reports_{month_number}'

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Prerequisites

Before running this script, ensure you have the following prerequisites:

- [Python](https://www.python.org/downloads/) installed on your machine.
- [Google Chrome](https://www.google.com/chrome/) web browser installed.
- ChromeDriver executable in the project directory. You can download it from [here](https://sites.google.com/chromium.org/driver/).
- Required Python libraries and packages installed. You can install them using `pip` by running `pip install -r requirements.txt`.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Place the ChromeDriver executable in the project directory.

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use this script, follow these steps:

1. Open a terminal and navigate to the project directory.

2. Run the script:

   ```bash
   python LAUSD_ADA_Reporting_Selenium.py
   ```

3. The script will automate various tasks related to attendance reporting for the specified schools.

## Configuration

You need to configure the script by providing your login credentials and specifying the list of schools you want to process.

- Open the `config.py` file and replace the placeholders with your username and password:

  ```python
  username = 'your_username'
  ps_pass = 'your_password'
  ```

- Update the `school_list` variable in `LAUSD_ADA_Reporting_Selenium.py` with the names of the schools you want to process.

---
