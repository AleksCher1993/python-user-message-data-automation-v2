import requests as req
import logging
import json
import os
import csv

def fetch_data(url):
    logging.info(f"Fetching data from {url}")
    try:
        with req.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
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

def create_data_dict(user, count):
    if user is None or count is None:
        logging.warning("No data provided to create data dictionary.")
        return None
    data_dict = {
        "user_id":user["id"],
        "name":user["name"],
        "email":user["email"],
        "city":user["address"]["city"],
        "posts_count":count
    }
    logging.info("Data dictionary created successfully.")
    return data_dict

def posts_count_dict(posts):
    if not posts:
        logging.warning("No posts data provided to create posts count dictionary.")
        return {}
    count_dict={}
    for post in posts:
        count_dict[post["userId"]] = count_dict.get(post["userId"], 0) + 1
    logging.info("Posts count dictionary created successfully.")
    return count_dict

def posts_users_list(users,posts_count_dict):
    if not users or not posts_count_dict:
        logging.warning("No data provided to create users posts list.")
        return []
    data_users_posts_list=[]
    for user in users:
        count = posts_count_dict.get(user["id"])
        item=create_data_dict(user, count)
        if item:    
            data_users_posts_list.append(item)
    logging.info("Users posts list created successfully.")
    return data_users_posts_list

def top_active_users(posts_users_list, top_n):
    if not posts_users_list:
        logging.warning("No users posts list provided to get top active users.")
        return []
    top_users=sorted(posts_users_list, key=lambda x: x["posts_count"] if x else 0, reverse=True)[:top_n]
    logging.info(f"Top {top_n} active users retrieved successfully.")
    return top_users

def write_csv_to_file(filename, data):
    logging.info(f"Writing CSV data to {filename}")
    try:
        if not data:
            logging.warning(f"No data to write to {filename}")
            return
        with open(filename, "w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"CSV data written successfully to {filename}")
    except IOError as e:    
        logging.error(f"Error writing CSV data to {filename}: {e}")



def main():
    os.makedirs("data", exist_ok=True)
    logging.basicConfig(filename="logs/app.log",level=logging.INFO,filemode='w',format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Application started")
    

    top_active_number=5
    URL_users="https://jsonplaceholder.typicode.com/users" #users API endpoint
    URL_posts="https://jsonplaceholder.typicode.com/posts" #posts API endpoint

    users_path="data/users.json"
    posts_path="data/posts.json"
    user_activity_path="data/user_activity.json"
    report_user_activity_path="data/report_user_activity.csv"
    report_posts_users_list_path="data/report_posts_users_list.csv"


    if not os.path.exists(users_path) or not os.path.exists(posts_path):
        logging.info("Data files do not exist. Fetching and writing data.")
        users = fetch_data(URL_users)
        posts = fetch_data(URL_posts)
        write_json_to_file(users_path, users)
        write_json_to_file(posts_path, posts)
    else:
        logging.info("Data files already exist. Skipping write operation.")
        users = read_json_from_file(users_path)
        posts = read_json_from_file(posts_path)

    posts_count_d = posts_count_dict(posts)
    posts_users_lst = posts_users_list(users, posts_count_d)
    top_active_usr=top_active_users(posts_users_lst, top_active_number)

    write_json_to_file(user_activity_path, top_active_usr)
    write_csv_to_file(report_user_activity_path, top_active_usr)
    write_csv_to_file(report_posts_users_list_path, posts_users_lst)
    logging.info("Application finished")

if __name__ == "__main__":
    main()