import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import traceback
import csv


chrome = webdriver.Chrome()

startTime = time.time()

chrome.get("https://www.instacart.ca/store/real-canadian-superstore/storefront")

outputFile = open("ScrapedFoods.txt", "w")

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

    chrome.execute_script("window.scrollTo(0, 0)")

scrollPage()

def scrollTo(element):
    chrome.execute_script(f"window.scrollTo(0, {element.location['y']-150})")

food_groups = chrome.find_elements(By.CLASS_NAME , "css-1dclc8o")

print(len(food_groups))
try : 
    for i in range(len(food_groups)):

        food_groups2 = chrome.find_elements(By.CLASS_NAME , "css-1dclc8o")

        #chrome.switch_to.window(chrome.window_handles[0])

        print(chrome.window_handles)

        scrollTo(food_groups2[i])  

        time.sleep(1.5)
    
        foodDict["food_group"+str(i)] = []

        while True:
            foods = food_groups2[i].find_elements(By.CLASS_NAME , "css-10klw3m")

            for j, food in enumerate(foods):

                try:

                    name = food.find_element(By.CLASS_NAME, "css-1o3m5pt").text

                except:
                    name = None
            
                try:
                    price = food.find_element(By.CLASS_NAME , "css-lkyxb9-PriceIa")
                    prices = price.find_elements(By.TAG_NAME, "span")

                    final_price = round(int(prices[1].text) + int(prices[2].text)/100, 2)

                except:
                    final_price = None
                    #print("price does not exist")

                try:
                    weight = food.find_element(By.CLASS_NAME , "css-s7rtpe").text
                except:
                    weight = None
                    #print("weight does not exist")

                currItem = FoodItem(name, final_price, weight)
                foodDict["food_group"+str(i)].append(currItem)
                outputFile.write(f"{name},{final_price},{weight}\n")

            try:
                
                carsolButton = food_groups2[i].find_element(By.CLASS_NAME, "css-elibrt-ListHeaderPageButton")
                carsolButton.click()
                time.sleep(0.5)
            except Exception:
                traceback.print_exc()
                break


    print(foodDict)
    outputFile.close()

except Exception:
    traceback.print_exc()
    print("-----------")
    print("Runtime :"  + str(time.time()-startTime))
        
    

        







        
        



