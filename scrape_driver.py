from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import csv

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Go to the Instagram login page
driver.get('https://www.instagram.com/accounts/login/')

# Wait for the username and password input fields to appear
username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))

# Type your username and password into the input fields
username_input.send_keys('pmtesting2023')
password_input.send_keys('1212qwer')

# 
profile_name = sys.argv[1] if len(sys.argv) > 1 else 'wholefoods'
num_posts = int(sys.argv[2]) if len(sys.argv) > 2 else 10

# Click the login button
# time.sleep(3000)
login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))
login_button.click()

# Give time to load
time.sleep(5)

# Wait for the first pop-up and click 'Not Now'
first_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x1i10hfl')))
first_popup.click()

# print("first popup clicked")

# Wait for the second pop-up and click 'Not Now'
second_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_a9--')))
second_popup.click()

# print("second popup clicked")

def scroll_page(times):
    # Scroll the page
    for i in range(times):
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for page to load

    # After scrolling, return the number of posts currently loaded on the page
    posts = driver.find_elements("class name", '_aagw')
    return len(posts)

# time.sleep(200)

try:
    search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Search"]')))
    search_button.click()
except:
    print("Search button not found.")

# Click on the search box and type 'wholefoods' into it
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]')))

search_box.send_keys(profile_name)
search_box.send_keys(Keys.ENTER)

# Wait for the Whole Foods profile to appear and click on it
profile = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/' + profile_name + '/"]')))
profile.click()

# Give time to load 
time.sleep(5)

# Scroll to the bottom:
# Calculate the number of times to scroll based on the number of posts to retrieve
scroll_times = num_posts // 12 if num_posts % 12 == 0 else num_posts // 12 + 1

data = []

# Initialize posts_processed to 0
posts_processed = 0

for i in range(scroll_times):
    
    # Scroll the page
    posts_loaded = scroll_page(1)  # Scroll once

    # Get all the post elements on the page
    posts = driver.find_elements("class name", '_aagw')

    for index in range(posts_processed, min(posts_processed + 12, num_posts)):

        # print("posts length: ", len(posts))
        # print("index: ", index)

        if index >= len(posts):
            
            # print("break triggered")
            break

        post = posts[index]
        # Click on the post
        try:
            # use JS to execute view
            driver.execute_script("arguments[0].scrollIntoView();", post)
            driver.execute_script("arguments[0].click();", post)
        except Exception as e:
            print(f"Error clicking the post: {e}")
            continue

        # Wait for the post to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(("class name", '_aatb')))

        # Get the date
        date = driver.find_element("class name", '_aaqe').get_attribute('datetime')

        # Get the link
        try:
            post_link = driver.current_url
        except Exception as e:
            print(f"Error getting link: {e}")
            post_link = None
        
        # Get the likes
        try:
            likes_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//span[contains(text(), 'likes')]/span")
                )
            )
            likes = likes_element.text
        except Exception as e:
            print(f"Error getting likes: {e}")
            likes = '0'

        # print(f'Likes: {likes}')

        # Add the data to the list
        data.append([date, likes, post_link])

        # time.sleep(2) 
        try:
            close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x78zum5 svg[aria-label="Close"]')))
            ActionChains(driver).move_to_element(close_button).click(close_button).perform()
            # print("post closed")
        except Exception as e:
            print(f"Error closing the post: {e}")
            continue

        print("Data added: ", data[len(data) - 1])

    # Update posts_processed
    posts_processed = posts_loaded

    # Sleep for a bit to ensure all posts have been properly loaded
    time.sleep(5)


# Close the browser
driver.quit()

print("Succcessfully scraped data.")

# Print the data
with open(f'{profile_name}_posts.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Likes", "Link"])  # writing headers
    writer.writerows(data)
