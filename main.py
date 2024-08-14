import instaloader
import os
import pickle
from datetime import datetime

INSTAGRAM_USERNAME = 'your_username'
INSTAGRAM_PASSWORD = 'your_password'

OLD_FOLLOWERS_FILE = 'old_followers.pkl'

def save_followers(followers, filename):
    with open(filename, 'wb') as file:
        pickle.dump(followers, file)

def load_followers(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return {}

def get_followers(username, loader):
    profile = instaloader.Profile.from_username(loader.context, username)
    followers = {}
    for follower in profile.get_followers():
        followers[follower.username] = follower.followed_at
    return followers

def main():
    user = input("instagram username ")
    
    loader = instaloader.Instaloader()
    
    try:
        loader.load_session_from_file(INSTAGRAM_USERNAME)
    except FileNotFoundError:
        print("logging in")
        loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        loader.save_session_to_file()
    
    old_followers = load_followers(OLD_FOLLOWERS_FILE)
    
    current_followers = get_followers(user, loader)
    
    new_followers = {user: date for user, date in current_followers.items() if user not in old_followers}
    
    if new_followers:
        print("new follower & its date")
        for follower, follow_date in new_followers.items():
            formatted_date = follow_date.strftime('%Y-%m-%d %H:%M:%S') if follow_date else 'Unknown'
            print(f'{follower}: {formatted_date}')
    else:
        print("no any new followers")
    
    save_followers(current_followers, OLD_FOLLOWERS_FILE)

if __name__ == "__main__":
    main()
