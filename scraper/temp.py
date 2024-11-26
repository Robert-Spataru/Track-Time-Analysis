def extract_links_by_state(driver, page_url, 
                           main_div_class="row mb-2 mt-3", 
                           state_div_class="col-6"):
    """
    Extract state links from a page.
    
    Args:
        driver: Selenium WebDriver instance.
        page_url (str): URL of the page to scrape.
        main_div_class (str): Class name of the main container div. Default is "row mb-2 mt-3".
        state_div_class (str): Class name of the state divs. Default is "col-6".
        
    Returns:
        dict: A dictionary where keys are state names and values are the links to their pages.
    """
    # Open the specified page
    driver.get(page_url)

    # Wait for the main div to be present
    main_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, '{main_div_class}')]"))
    )

    # Find all sub-divs representing states
    state_divs = main_div.find_elements(By.XPATH, f".//div[contains(@class, '{state_div_class}')]")

    # Initialize dictionary to store links by state
    links_by_state = {}

    for state_div in state_divs:
        try:
            # Get the state name
            state_name_element = state_div.find_element(By.XPATH, ".//small")
            state_name = state_name_element.text.strip()
            
            # Skip any unwanted entries
            if state_name != "Overseas":
                # Get the href link
                link_element = state_div.find_element(By.XPATH, ".//a[@class='d-block']")
                href = link_element.get_attribute("href")
                
                # Add to dictionary
                links_by_state[state_name] = href
                
        except Exception as e:
            print(f"Error processing state div: {e}")

    return links_by_state

'''
# URL for the high school page (replace `url_list[0]` with the actual URL if needed)
high_school_link = url_list[0]  # Assuming url_list[0] contains the high school link

# Extract the state links for high school
high_school_links = extract_links_by_state(driver, high_school_link)

# Print the result
print("High School Links:", high_school_links)
'''


def extract_meets_by_state(driver, state_meet_links, 
                           main_div_xpath="//div[contains(@class, 'list-group list-group-flush')]", 
                           sub_child_class="list-group-item-action"):
    """
    Extracts track and field meet links by state from a webpage.

    Parameters:
    - driver: Selenium WebDriver instance.
    - state_meet_links: Dictionary where keys are state names and values are URLs for each state's meet page.
    - main_div_xpath (str, optional): XPath to the main div containing the meet links. Defaults to a commonly used structure.
    - sub_child_class (str, optional): Class name of the child elements containing the meet links. Defaults to "list-group-item-action".

    Returns:
    - Dictionary: A dictionary where keys are state names and values are lists of meet links for that state.
    """
    # Initialize a dictionary to store meet links by state
    meets_by_state_dict = {}
    
    # Loop through each state and its corresponding link
    for state, link in state_meet_links.items():
        # Navigate to the state's meet page
        driver.get(link)
        
        # Wait for the main div to be present on the page
        main_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, main_div_xpath))
        )
        
        # Find all child elements within the main div that match the specified class
        sub_child_elements = main_div.find_elements(By.XPATH, f".//a[contains(@class, '{sub_child_class}')]")
        
        # Extract href attributes (links) from the child elements
        links = [element.get_attribute("href") for element in sub_child_elements]
        
        # Add the state and its associated meet links to the dictionary
        meets_by_state_dict[state] = links
    
    # Return the dictionary containing meet links by state
    return meets_by_state_dict
'''
meets_by_state = extract_meets_by_state(driver, high_school_links)
print(meets_by_state["Alabama"])
'''

def extract_event_links(driver, meets_by_state, 
                        target_events=["100 Meters", "200 Meters", "400 Meters"],
                        genders=["Male", "Female"],
                        main_div_xpath="//div[@class='col-sm-6 mb-3 ng-star-inserted' and .//h4[contains(text(), '{}')]]",
                        sub_child_class=".//a[contains(@href, 'results') and span[contains(@class, 'b') and text() = 'Varsity']]"):
    """
    Extracts event links organized by state, meet, and gender.
    
    Args:
        driver: Selenium WebDriver instance.
        meets_by_state: A dictionary where keys are state names and values are lists of meet URLs.
        target_events: List of event names to filter for (default: ["100 Meters", "200 Meters", "400 Meters"]).
        genders: List of genders to extract data for (default: ["Male", "Female"]).
        main_div_xpath: XPath template for locating gender sections (default provided).
        sub_child_class: XPath for locating specific event links within the gender section (default provided).
    
    Returns:
        events_by_meet_by_state_dict: Nested dictionary with states as keys and dictionaries of meets and event links as values.
    """
    events_by_meet_by_state_dict = {}

    for state, state_meets_list in meets_by_state.items():
        # Initialize the state-level dictionary
        events_by_meet_by_state_dict[state] = {}

        for meet_link in state_meets_list:
            driver.get(meet_link)
            
            # Initialize the meet-level dictionary
            meet_event_links = {}

            for gender in genders:
                # Format the XPath for the current gender
                gender_section_xpath = main_div_xpath.format(gender)
                
                try:
                    # Locate the gender section
                    gender_section = driver.find_element(By.XPATH, gender_section_xpath)
                    
                    # Find event links within the gender section
                    event_links = gender_section.find_elements(By.XPATH, sub_child_class)
                    
                    # Filter links for the target events
                    filtered_links = [link.get_attribute('href') for link in event_links 
                                      if any(event in link.text for event in target_events)]
                    
                    # Store the filtered links under the gender
                    meet_event_links[gender] = filtered_links
                
                except Exception as e:
                    print(f"Error processing {gender} section for {meet_link}: {e}")
                    meet_event_links[gender] = []  # Default to empty list if section not found
            
            # Store the meet event links under the meet link
            events_by_meet_by_state_dict[state][meet_link] = meet_event_links

    return events_by_meet_by_state_dict

'''
events_by_meet_by_state_dict = extract_event_links(driver, meets_by_state)
print(events_by_meet_by_state_dict["Alabama"])
'''

def extract_data_into_table(driver, events_by_meet_by_state_dict, table_dataframe):
    pass


def loop_through_years(driver):
    pass


