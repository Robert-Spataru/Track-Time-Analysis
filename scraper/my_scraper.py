#selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#beutiful soup import
from bs4 import BeautifulSoup
import requests


def extract_dropdown_urls(driver, dropdown_button_xpath, 
                          dropdown_menu_class_name, 
                          dropdown_item_class_name):
    """
    Extracts URLs from a dropdown menu and returns them as a list.

    Parameters:
        driver: WebDriver instance
        dropdown_button_xpath (str): XPath for the dropdown button
        dropdown_menu_class_name (str): Class name of the dropdown menu
        dropdown_item_class_name (str): Class name of the dropdown items

    Returns:
        list: List of URLs extracted from the dropdown menu
    """
    # Wait for the dropdown button and click it
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, dropdown_button_xpath))
    )
    dropdown_button.click()

    # Wait for the dropdown menu to be visible
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, dropdown_menu_class_name))
    )

    # Store the list of dropdown items
    dropdown_items = dropdown_menu.find_elements(By.CLASS_NAME, dropdown_item_class_name)
    url_list = []

    # Loop through dropdown items and extract URLs
    for dropdown in dropdown_items:
        try:
            dropdown.click()

            # Wait for the URL to change and store the current page URL
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            current_url = driver.current_url
            url_list.append(current_url)
            print("Actual page URL:", current_url)

            # Navigate back and reset the dropdown
            driver.back()
            dropdown_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, dropdown_button_xpath))
            )
            dropdown_button.click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, dropdown_menu_class_name))
            )
        except Exception as e:
            print(f"Error processing dropdown item: {e}")

    return url_list


def extract_links_by_state(page_url, main_div_class="row mb-2 mt-3", state_div_class="col-6"):
    """
    Extract state links from a page using BeautifulSoup.

    Args:
        page_url (str): URL of the page to scrape.
        main_div_class (str): Class name of the main container div. Default is "row mb-2 mt-3".
        state_div_class (str): Class name of the state divs. Default is "col-6".

    Returns:
        dict: A dictionary where keys are state names and values are the links to their pages.
    """
    # Send a request to the page and parse the HTML content
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main div and state divs
    main_div = soup.find('div', class_=main_div_class)
    state_divs = main_div.find_all('div', class_=state_div_class)

    # Initialize dictionary to store links by state
    links_by_state = {}

    for state_div in state_divs:
        try:
            # Get the state name
            state_name_element = state_div.find('small')
            state_name = state_name_element.text.strip()

            # Skip any unwanted entries
            if state_name != "Overseas":
                # Get the href link
                link_element = state_div.find('a', class_='d-block')
                href = link_element['href']
                
                # Add to dictionary
                links_by_state[state_name] = href
                
        except Exception as e:
            print(f"Error processing state div: {e}")

    return links_by_state


def extract_meets_by_state(state_meet_links, main_div_class="list-group list-group-flush", sub_child_class="list-group-item-action"):
    """
    Extracts track and field meet links by state from a webpage using BeautifulSoup.

    Args:
        state_meet_links (dict): A dictionary where keys are state names and values are URLs for each state's meet page.
        main_div_class (str, optional): Class name of the main div containing the meet links. Defaults to "list-group list-group-flush".
        sub_child_class (str, optional): Class name of the child elements containing the meet links. Defaults to "list-group-item-action".

    Returns:
        dict: A dictionary where keys are state names and values are lists of meet links for that state.
    """
    # Initialize a dictionary to store meet links by state
    meets_by_state_dict = {}

    # Loop through each state and its corresponding link
    for state, link in state_meet_links.items():
        # Send a request to the state's meet page and parse the HTML content
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main div containing the meet links
        main_div = soup.find('div', class_=main_div_class)

        # Find all child elements within the main div that match the specified class
        sub_child_elements = main_div.find_all('a', class_=sub_child_class)

        # Extract href attributes (links) from the child elements
        links = [element['href'] for element in sub_child_elements]

        # Add the state and its associated meet links to the dictionary
        meets_by_state_dict[state] = links

    # Return the dictionary containing meet links by state
    return meets_by_state_dict


def extract_event_links(meets_by_state, target_events=["100 Meters", "200 Meters", "400 Meters"],
                        genders=["Male", "Female"], 
                        main_div_class="col-sm-6 mb-3 ng-star-inserted",
                        sub_child_class="b"):
    """
    Extracts event links organized by state, meet, and gender using BeautifulSoup.

    Args:
        meets_by_state (dict): A dictionary where keys are state names and values are lists of meet URLs.
        target_events (list): List of event names to filter for (default: ["100 Meters", "200 Meters", "400 Meters"]).
        genders (list): List of genders to extract data for (default: ["Male", "Female"]).
        main_div_class (str): Class name for the gender sections (default: "col-sm-6 mb-3 ng-star-inserted").
        sub_child_class (str): Class name for locating specific event links within the gender section (default: "b").
    
    Returns:
        dict: Nested dictionary with states as keys and dictionaries of meets and event links as values.
    """
    events_by_meet_by_state_dict = {}

    for state, state_meets_list in meets_by_state.items():
        # Initialize the state-level dictionary
        events_by_meet_by_state_dict[state] = {}

        for meet_link in state_meets_list:
            # Send a request to the meet page and parse the HTML content
            response = requests.get(meet_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize the meet-level dictionary
            meet_event_links = {}

            for gender in genders:
                # Find the gender section based on the class and gender
                gender_section = soup.find('div', class_=main_div_class, string=gender)

                try:
                    # Find event links within the gender section
                    event_links = gender_section.find_all('a', class_=sub_child_class)

                    # Filter links for the target events
                    filtered_links = [link['href'] for link in event_links 
                                      if any(event in link.text for event in target_events)]
                    
                    # Store the filtered links under the gender
                    meet_event_links[gender] = filtered_links
                
                except Exception as e:
                    print(f"Error processing {gender} section for {meet_link}: {e}")
                    meet_event_links[gender] = []  # Default to empty list if section not found
            
            # Store the meet event links under the meet link
            events_by_meet_by_state_dict[state][meet_link] = meet_event_links

    return events_by_meet_by_state_dict