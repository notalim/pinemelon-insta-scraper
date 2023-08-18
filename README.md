# Instagram Data Scraper

This Python application utilizes Selenium to automatically navigate and scrape data from specific Instagram profiles. It gathers key information about individual posts, including:

- The date the post was made
- The number of likes
- The direct URL to the post

## How it Works

1. First, the script opens the Chrome browser and logs into Instagram using the provided credentials.
2. Then, it navigates to the specified Instagram profile.
3. The script then scrolls through the profile and opens each post one by one.
4. It waits for the post data to load, then scrapes the post's date, likes, and URL.
5. This data is added to a list.
6. The process is repeated for a specified number of posts or until there are no more posts left.
7. Finally, the script closes the browser and prints the scraped data.

## Usage Example

Suppose we want to scrape 10 posts from the profile '@example_profile'. Follow the steps below:

1. Update the `scrape_driver.py` script with your Instagram credentials:
   ```python
   username_input.send_keys('your_username')
   password_input.send_keys('your_password')
   ```
2. Run `scrape_driver.py` in the terminal with the desired profile and number of posts as arguments:
bash
```
$ python scrape_driver.py example_profile 10
```

After executing these steps, the scraped data will be stored in a CSV file named `example_profile_posts.csv` in the same directory.