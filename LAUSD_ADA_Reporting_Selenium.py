# goal is to refresh attendace, and run the Attendance Reports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException, StaleElementReferenceException
import os
import time
import logging
import re
import numpy as np
from config import ps_pass
from bs4 import BeautifulSoup

start_date = '08/14/2023'
end_date = '09/08/2023'

logging.basicConfig(filename='LAUSD_Reporting.log', level=logging.INFO,
                   format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',force=True)

logging.info('\n\n-------------LAUSD Reporting Log')


# Specify the download directory
download_directory = os.getcwd()

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : download_directory,
         'profile.default_content_setting_values.automatic_downloads': 1,
         'profile.content_settings.exceptions.automatic_downloads.*.setting': 1}
chrome_options.add_experimental_option('prefs', prefs)

chrome_service = Service(os.getcwd() + '\\ChromeDriver\\chromedriver.exe')
driver = webdriver.Chrome(service = chrome_service, options=chrome_options)
url = 'https://ps.greendot.org/admin/pw.html'

username = 'samuel.taylor'
password = ps_pass



school_list = ['Animo Leadership CHS ' ,
            'Animo Inglewood CHS ',
            'Oscar De la Hoya Animo CHS ',
            'Animo South L.A. CHS ',
            'Animo Venice CHS ',
            'Animo Pat Brown CHS ',
            'Animo Ralph Bunche CHS ',
            'Animo Jackie Robinson CHS ',
            'Animo Watts College Preparatory Academy ',
            'Alain Leroy Locke College Preparatory Academy ',
            'Animo James B Taylor Middle School ',
            'Animo Jefferson Charter Middle School ',
            'Animo Legacy Charter Middle School ',
            'Animo Ellen Ochoa Middle School ',
            'Animo Mae Jemison Middle School ',
            'Animo Florence-Firestone CMS ',
            'Animo City of Champions Charter High School ',
            'Animo Compton Charter School ']


driver.get(url)

# ----------------------------------------------------

def login_func():

    username_field = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'fieldUsername'))
                )

    username_field.send_keys(username)

    field_pass = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'fieldPassword'))
                )

    field_pass.send_keys(password)

    login_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'btnEnter'))
                )
    try:
        login_button.click()
        logging.info('Logged into PS platform')
    except:
        logging.info('Unable to log into PS platform')


# -----------------------choose school-------------------------------

def school_choice(what_school):
    
    print(what_school)

    school_dropdown = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="school_picker_adminSchoolPicker_toggle_btn"]/pds-icon'))
                    )

    school_dropdown.click()

    school_selection = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{what_school}')]"))
                    )

    try:
        school_selection.click()
        logging.info(f'School selection occured - {what_school}')
    except:
        logging.info(f'Unable to select school - {what_school}')


# ----------------------Submit attendance refresh------------------------------
def submit_attendance_refresh():


    try:
        attendance_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navAttStatus"]'))
        )
        attendance_button.click()

    except StaleElementReferenceException:
        # Re-locate the element and then click it
        attendance_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="navAttStatus"]'))
        )
        attendance_button.click()


    refresh_attendance = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="content-main"]/div[3]/table/tbody/tr[4]/td[1]/a'))
                        )

    refresh_attendance.click()

    start_date_input = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "param_startdate"))
                        )

    start_date_input.clear()
    start_date_input.send_keys(start_date)

    end_date_input = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "param_enddate"))
                        )

    end_date_input.clear()
    end_date_input.send_keys(end_date)

    submit_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'btnSubmit'))
                )

    try:
        submit_button.click()
        logging.info(f'Attendance refreshed for {start_date} to {end_date}')
    except:
        logging.info(f'Unable to refresh attendance for {start_date} to {end_date}')

# -------------------run attendance summary by grade reports------------------------

def run_attendance_summary_grade_reports():

    system_reports = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, 'navSysReports'))
            )

    system_reports.click()

    state_tab = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, '//*[@id="reporttypes"]/li[3]/a'))
                            )

    state_tab.click()

    attendance_summary_grade_reports = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, '//*[@id="content-main"]/div[2]/div[1]/div[1]/table[2]/tbody/tr[5]/td[1]/a'))
                                
                            )


    attendance_summary_grade_reports.click()


    remove_block = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[5]/form/div[1]/table/tbody/tr[15]/td[2]/div[2]/div[1]/input'))
                    )

    remove_block.click()

    user_defined_start_date_input = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "reportingPeriodUserDefinedStartDate"))
                        )

    user_defined_start_date_input.send_keys(start_date)

    user_defined_end_date_input = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "reportingPeriodUserDefinedEndDate"))
                        )

    user_defined_end_date_input.send_keys(end_date)

    submit_attendance_summary_by_grade = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "submitReportSDKRuntimeParams"))
                        )
    try:
        submit_attendance_summary_by_grade.click()
        logging.info('Attendance summary by grade submitted')
    except:
        logging.info('Unable to submit attendance summary by grade')

    # -----------------------------------------------------------------

#HS this runs once
#MS it will run three times 6, 6-8,  & 7-8
#Unless it is Compton then it will run once for all grade levels, 
# once for grade 6, once for grades 7-8 and once for grades 9-12.

    
def get_ada_adm_by_date():

    system_reports_button = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, "//a[@title='Run system reports']"))
                            )

    system_reports_button.click()

    ada_adm_date_button = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.LINK_TEXT, "ADA/ADM by Date"))
                            )

    ada_adm_date_button.click()


    user_defined_start_date_input = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "param_startdate"))
                        )
    user_defined_start_date_input.clear()
    user_defined_start_date_input.send_keys(start_date)

    user_defined_end_date_input = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.NAME, "param_enddate"))
                        )
    user_defined_end_date_input.clear()
    user_defined_end_date_input.send_keys(end_date)

    submit_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.ID, 'btnSubmit'))
                )
    try:
        submit_button.click()
        logging.info('ADA by ADM by date has been submitted')
    except:
        logging.info('ADA by ADM by date has NOT been submitted')

# --------------------------------------------------------------------

def parse_ada_adm_report():

    #this just needs more time

    open_ada_adm_report = WebDriverWait(driver, 30).until(
                                    EC.element_to_be_clickable((By.XPATH, '//*[@id="reportq"]/table/tbody/tr[1]/td[6]/a'))
                                )
    try:
        open_ada_adm_report.click()
        logging.info('Opened ADA ADM report')
    except:
        logging.info('Unable to open ADA ADM report')


    # Get the list of window handles
    window_handles = driver.window_handles

    # Switch to the newly opened window
    new_window_handle = window_handles[-1]
    driver.switch_to.window(new_window_handle)

    # Step 3: Use Selenium to get the page source
    page_source = driver.page_source

    # Step 4: Use BeautifulSoup to parse the page source and extract the data
    soup = BeautifulSoup(page_source, 'html.parser')

    header = soup.find('td', align='right').text

    #parse the ada_adm_report into a pandas frame
    table = soup.find('div', {'align': 'center'}).find('table')

    # Extract table rows (data)
    data = []
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        if row_data:
            data.append(row_data)

    df = pd.DataFrame(data[1: -3], columns = data[0])

    totals = pd.DataFrame(data[-2:])


    totals.insert(0, 'NaN_1', np.nan)
    totals.insert(0, 'NaN_2', np.nan)
    totals.iloc[0, 0] = header

    new_names = dict(zip(list(totals.columns), list(df.columns)))
    totals = totals.rename(columns = new_names)

    df = pd.concat([df, totals], ignore_index=True)

    all_ada_adm_reports.append(df)

# ------------------------------------------------

def download_attendance_summary_report():

    # Get the list of window handles
    window_handles = driver.window_handles

    # Switch to the newly opened window
    new_window_handle = window_handles[0]
    driver.switch_to.window(new_window_handle)


    report_works_button = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.LINK_TEXT, "ReportWorks"))
                            )

    report_works_button.click()

    # -----------------------------------
    #delete the AttendanceSummaryByGrade prior to downlaoding the new file
    # Get a list of files in the working directory
    files_in_directory = os.listdir()

    # # Iterate through the files and delete those containing the substring
    for file_name in files_in_directory:
        if 'AttendanceSummaryByGrade' in file_name:
            os.remove(file_name)
            print(f"File '{file_name}' containing the substring 'AttendanceSummaryByGrade' deleted.")
            logging.info(f"File '{file_name}' containing the substring 'AttendanceSummaryByGrade' deleted.")
        else:
            pass

    # -----------------------
    #recursively try to download the AttendanceSummaryByGrade in order to parse

    max_attempts = 4
    attempts = 0

    while attempts < max_attempts:
        try:
             
            running_or_complete = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, '//*[@id="queuecontent"]/table[1]/tbody/tr[2]/td[8]'))
                            )

            if "Running" in running_or_complete.text or "Pending" in running_or_complete.text:
                

                print("Attendance summary by grade still loading. Refreshing web page")
                time.sleep(10)
                driver.refresh()
                attempts += 1
                print('Attempt recorded')
            else:
                print("Running or Pending is not in the tag. Downloaded the report")

                download_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="queuecontent"]/table/tbody/tr[2]/td[7]/a/div'))
                    )
                download_button.click()

                #break out of while loop because report has been downloaded. 
                break

        #the running or complete element will not even be present if report is ready
        except NoSuchElementException:
            print("Running or complete not available moving past")
            
            download_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="queuecontent"]/table/tbody/tr[2]/td[7]/a/div'))
                    )
            try:
                download_button.click()
                logging.info('Downloaded Attendance Summary Report')
            except:
                logging.info('Unable to download Attendance Summary Report - Report Failed')

# -------------------------------------------------------------

def scrape_attendance_summary_report():

    time.sleep(2)

    # Open the HTML file in read mode
    with open('AttendanceSummaryByGrade.html', "r", encoding="utf-8") as html_file:
        # Read the contents of the HTML file
        html_content = html_file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")


    #parse the ada_adm_report into a pandas frame
    table = soup.find('div', {'align': 'center'}).find('table')

    # Extract table rows (data)
    data = []
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        if row_data:
            data.append(row_data)

    df = pd.DataFrame(data[1: ], columns = data[0])

    # -------------------------------
    # Find all the headers and insert in at the end
    text_content = [tag.get_text() if tag.name == "b" else tag.next_sibling.strip() for tag in soup.find_all(["b", "br"])]

    temp = pd.DataFrame(text_content)[0:6]
    temp = temp.loc[temp[0] != '']

    # Determine how many blank columns to add
    columns_to_add = 13 - len(temp.columns)

    # Add blank columns to the right
    for i in range(columns_to_add):
        temp[len(temp.columns)] = ""

    temp = temp.rename(columns = dict(zip(list(temp.columns), list(df.columns))))

    df = pd.concat([df, temp], ignore_index=True)

    all_attendance_summary_reports.append(df)
    
# ----------------------------Calling all functions into one pipeline------------------------ 

all_attendance_summary_reports = []
all_ada_adm_reports = []

def process(what_school, iteration):
    #If it is the first time login, otherwise go back to the homepage and change the selection 
    if iteration == 0:
        login_func()
    else:
        pass
    school_choice(what_school)
    submit_attendance_refresh()
    run_attendance_summary_grade_reports()
    get_ada_adm_by_date()
    parse_ada_adm_report()
    download_attendance_summary_report()
    scrape_attendance_summary_report()

    #once process has gone through once. Go back to the top
    ps_homepage = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="branding-powerschool"]/img'))
                )
    try:
        ps_homepage.click()
        logging.info('Back to the homepage to restart')
    except:
        logging.info('Unable to get back to the homepage')
    
#Calling the first 3 schools from the school list
for index, value in enumerate(school_list[:3]):
    process(value, index)

all_attendance_summary_reports = pd.concat(all_attendance_summary_reports)
all_ada_adm_reports = pd.concat(all_ada_adm_reports)