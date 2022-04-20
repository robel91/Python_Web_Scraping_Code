
import pyodbc

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

#create a connection and cursor 
conn = pyodbc.connect(driver ='{SQL SERVER}',
                      Server ='18.225.7.23',
                      database ='MSIS-415',
                      uid="sa",
                      pwd="Rahelhaftey18$")
cursor = conn.cursor()

try:
     #create table in MS server
    SQL="create table car_for_sale\
               (condition varchar(50) ,\
                description varchar(100),\
                milage int ,\
                price int ,  \
                dealer varchar(50),\
                dealer_star_rate varchar(50))"
    print(SQL)
    cursor.execute(SQL)
    conn.commit()
except:
    print("The table is already created")

url = "https://www.cars.com/shopping/boston-ma/"
driver = webdriver.Chrome()
driver.get(url)

page=0
while True:
    time.sleep(2)
    page+=1
    print("current page is",page)
    dropdown = driver.find_element(By.ID,'location-distance')
    radius = Select(dropdown)
    radius.select_by_visible_text('All miles from')
    time.sleep(2)
    
    car_blocks = driver.find_elements(By.CLASS_NAME,"vehicle-details")

    for car_block in car_blocks:
    
        #car condition
        condition = car_block.find_element(By.CLASS_NAME,"stock-type")
        #for conditions in condition:
        print(condition.text)
        
        #car description
        description = car_block.find_element(By.CLASS_NAME,'title')
        #description = description[0:4].split()
        print(description.text)
    
        #milage
        milage = car_block.find_element(By.CLASS_NAME,'mileage').text
        milage = milage.split()
        milage = milage[0:1]
        print(milage)
        
        #price of the car
        price = car_block.find_element(By.XPATH,'//span[@class="primary-price"]')
        # for prices in price:
        print(price.text)
        # split_str = miles.split()
        # #print(split_str)
        # only_num = split_str[0:1]
        # print(only_num)
    
    
            
    
        
    
        #dealer who sell it
        dealer=""
        try:
            dealer = car_block.find_element(By.CLASS_NAME,'dealer-name')
        except:
            dealer = car_block.find_element(By.CLASS_NAME,'seller-name')
            
        #for dealers in dealer:
        print(dealer.text)
             
    
        #the dealer star rate
        dealer_star_rate = car_block.find_element(By.XPATH,'//span[@class="sds-rating__count"]')
        #for rates in rate:
        print(dealer_star_rate.text)
        
        
        SQL= "INSERT INTO car_for_sale Values('"+condition.text+"','"+description.text+"',"\
        +milage[0].replace(",","")+","+price.text.replace(",","").replace("$","")+",'"+dealer.text+"','"+dealer_star_rate.text+"')"
        print(SQL)
        cursor.execute(SQL)
        conn.commit()

    #next page button
    
    try:
        
    
        button = driver.find_element(By.ID,'next_paginate')
        button.click() 
        time.sleep(2)
        
    except:
        print('ended!')
        break   
        
