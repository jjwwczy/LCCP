Environment Configuration：python3.10.11 + pycharm
Required Packages：requests, lxml, bs4, pdfplumber, selenium, time, re, pandas, pdfkit, pyperclip, glob, os, docx, webdriver_manager, pinyin, wkhtmltopdf

Code Description：
main.py is the main execution file that allows you to specify search keywords and the number of pages to search. It sequentially performs three steps for each city: retrieving webpage URLs, filtering webpage content, and scoring based on the webpage content.
utils.py serves as a function library, providing all the necessary functions required by main.py to execute the three steps.


MIT License

Copyright (c) 2023 [Haijun Bao, Xiangrui Xu, Zeyu Cao, Ming Li, Yang Guo]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
