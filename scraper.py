import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


chrome = webdriver.Chrome()

chrome.get("https://www.instacart.ca/store/real-canadian-superstore/storefront")

soup = BeautifulSoup(chrome.page_source, 'html.parser')

class FoodItem : 
    def __init__(self, name, price, weight) -> None:
        self.name = name
        self.price = price
        self.weight = weight


    def __repr__(self):
        return (f"{self.name} price: {self.price} weight: {self.weight}")

foodDict = {}

def scrollPage():

    
    lastHeight = chrome.execute_script("return document.body.scrollHeight")

    while True:
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        newHeight = chrome.execute_script("return document.body.scrollHeight")

        if newHeight == lastHeight:
            break

        lastHeight = newHeight

#scrollPage()

#chrome.execute_script("window.scrollTo(0, 0)")

print(len(chrome.find_elements(By.CLASS_NAME, 'css-elibrt-ListHeaderPageButton')))

food_groups = chrome.find_elements(By.CLASS_NAME , "css-1dclc8o")
bs_food_groups = soup.find_all("div", class_="css-1dclc8o")

print(len(bs_food_groups))

for i, food_group in enumerate(bs_food_groups):
    sel_food_group = food_groups[i]

    time.sleep(1.5)
   
    foodDict["food_group"+str(i)] = []

    while True:
        foods = food_group.find_all("li", class_="css-10klw3m")

        for j, food in enumerate(foods):

            try:
                name = food.find("span", class_="css-1o3m5pt").string
            except:
                name = None

            try:

                price = food.find("div" , class_="css-lkyxb9-PriceIa")
                prices = price.contents
                final_price = round(int(prices[1].string) + int(prices[2].string)/100, 2)

            except:
                price = None
                #print("price does not exist")

            try:
                weight = food.find_element("div" , class_="css-s7rtpe").string
            except:
                weight = None
                #print("weight does not exist")


            currItem = FoodItem(name, final_price, weight)
            foodDict["food_group"+str(i)].append(currItem)
        
        try:
            carsolButton = sel_food_group.find_element(By.CLASS_NAME, "css-elibrt-ListHeaderPageButton")
            print(f"button found on row " + {i})
            carsolButton.click()
            print(f"click on row  + {i} +  sussfuell")
            time.sleep(1)
        except:
            print("while loop broken")
            break
    

        







        
        



