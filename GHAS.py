#!/usr/bin/env python3

import csv
import time
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def handle_beforeunload(dialog):
    dialog.accept()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    page.on('beforeunload', handle_beforeunload)

    #Login to Github - user & password obfuscation 
    page.goto('https://github.com/login')
    page.fill('input#login_field', 'USER')
    page.fill('input#password', 'PASSWORD')
    page.click('input[type=submit]')
    time.sleep(25)

    #Create CSV file
    csv_file = open('C:\\Users\\(SHERWIN USER ID)\\OneDrive - Sherwin-Williams\\Desktop\\test.csv', 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Repository', 'Dependabot', 'Code Scanning', 'Secret Scanning'])

    #Redirect Into Github Security Coverage
    for page_number in range(1,n):
        page_url = f'https://github.com/orgs/sherwin-williams-co/security/coverage?page={page_number}'
        page.goto(page_url)

        if page_number == 1:
            page.click('button[type=submit]') 
        page.is_visible('#coverage-data')
    
        html = page.inner_html('#coverage-data')
        soup = BeautifulSoup(html, 'html.parser')

        # Seperate Data by Repository & Define Function
        page.is_visible('#coverage-data')
        repository_divs = soup.find_all('div', class_='flex-1 d-flex flex-wrap')

        for div in repository_divs:
            repository_name = div.find('a', class_='Link--primary text-bold d-block').get_text(strip=True)
    
            dependabot_setup = div.find('span', text='Dependabot').find_next_sibling('span').get_text(strip=True)

            codescanning_element = div.find('span', text='Code scanning')
            if codescanning_element:
                codescanning_setup= codescanning_element.find_next('span').get_text(strip=True)
            else:
                codescanning_setup= "Not Found"
            secret_setup = div.find('span', text='Secret scanning').find_next_sibling('span').get_text(strip=True)

            csv_writer.writerow([repository_name, dependabot_setup, codescanning_setup, secret_setup])

csv_file.close()

with open('C:\\Users\\(SHERWIN USER ID)\\OneDrive - Sherwin-Williams\\Desktop\\temp.csv', 'r+') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)

    header.extend(['GHAS','Secret Scanning Push Protection'])

    test_file = open('C:\\Users\\(SHERWIN USER ID)\\OneDrive - Sherwin-Williams\\Desktop\\GHAS_SETUP.csv', 'w', newline='')
    csv_writer = csv.writer(test_file)
    csv_writer.writerow(header)

    for row in csv_reader:
        repository_name = row[0]

        owner = 'sherwin-williams-co'
        repo = repository_name

        ghas_url = f'https://api.github.com/repos/{owner}/{repo}'

        headers = {
                'Authorization': 'Token GITHUB_TOKEN'
            }

        response = requests.get(ghas_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            advanced_security = data.get('security_and_analysis')

            if advanced_security and advanced_security.get('advanced_security') and advanced_security['advanced_security'].get('status') == 'enabled':
                ghas_status = 'Enabled'
            else:
                ghas_staus = 'Not Enabled'
            if advanced_security and advanced_security.get('secret_scanning_push_protection') and advanced_security['secret_scanning_push_protection'].get('status') == 'enabled':
                secret_scanning = 'Enabled'
            else:
                secret_scanning = 'Not Enabled' 
            row.extend([ghas_status, secret_scanning])
        
        csv_writer.writerow(row)

    test_file.close()

    with open('C:\\Users\\(SHERWIN USER ID)\\OneDrive - Sherwin-Williams\\Desktop\\GHAS_SETUP.csv', 'r') as temp_file:
        csv_file.write(test_file.read())

    csv_file.truncate
