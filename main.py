import requests as req
import logging
import json
import os
def fetch_data(url):
    logging.info(f"Fetching data from {url}")
    try:
        with req.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            print(response.json())
            logging.info(f"Data fetched successfully from {url}")
            return response.json()
    except req.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

def write_json_to_file(filename, data):
    logging.info(f"Writing json data to {filename}")
    try:
        if data is None:
            logging.warning(f"No data to write to {filename}")
            return
        with open(filename,"w",encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logging.info(f"Json data written successfully to {filename}")
    except IOError as e:    
        logging.error(f"Error writing json data to {filename}: {e}")

def read_json_from_file(filename):
    logging.info(f"Reading json data from {filename}")
    try:
        with open(filename,"r",encoding="utf-8") as file:
            data=json.load(file)
            logging.info(f"Json data read successfully from {filename}")
            return data
    except IOError as e:    
        logging.error(f"Error reading json data from {filename}: {e}")
        return None

def main():
    logging.basicConfig(filename="logs/app.log",level=logging.INFO,filemode='w',format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Application started")

    URL_users="https://jsonplaceholder.typicode.com/users" #users API endpoint
    URL_posts="https://jsonplaceholder.typicode.com/posts" #posts API endpoint

    
    if not os.path.exists("datas/users.json") and not os.path.exists("datas/posts.json"):
        logging.info("Data files do not exist. Fetching and writing data.")
        users = fetch_data(URL_users)
        posts = fetch_data(URL_posts)
        write_json_to_file("datas/users.json", users)
        write_json_to_file("datas/posts.json", posts)
    else:
        logging.info("Data files already exist. Skipping write operation.")
        users = read_json_from_file("datas/users.json")
        posts = read_json_from_file("datas/posts.json")
    
    

    logging.info("Application finished")

if __name__ == "__main__":
    main()