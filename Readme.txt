Environment Configuration：python3.10.11 + pycharm
Required Packages：requests, lxml, bs4, pdfplumber, selenium, time, re, pandas, pdfkit, pyperclip, glob, os, docx, webdriver_manager, pinyin, wkhtmltopdf

Code Description：
main.py is the main execution file that allows you to specify search keywords and the number of pages to search. It sequentially performs three steps for each city: retrieving webpage URLs, filtering webpage content, and scoring based on the webpage content.
utils.py serves as a function library, providing all the necessary functions required by main.py to execute the three steps.