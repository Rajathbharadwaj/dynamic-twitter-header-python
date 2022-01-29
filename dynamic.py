import tweepy
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFilter
from tqdm import tqdm
import requests
load_dotenv()

def get_twitter_api():
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"))
    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
    return tweepy.API(auth)


def get_images(names, links):
    for i, link in tqdm(enumerate(links)):
        response = requests.get(link)
        write_to_file(names[i], response.content)

def write_to_file(name, content):
    file = open(f"{name}.jpg", "wb")
    file.write(content)
    file.close()
        
def get_image_header(header, user1, user2, user3):
    back_im = header.copy()
    back_im.paste(user1, (1135, 400))
    back_im.paste(user2, (1252, 399))
    back_im.paste(user3, (1367, 399))
    back_im.save('pasted-twitter-banner.png', quality=95)
    back_im
    print("Done!")


if __name__ == "__main__":
    api = get_twitter_api()
    followers = api.get_followers(count=3)
    profiles = {}
    profiles["followers"]= [{"username": follower.screen_name, "photo": follower.profile_image_url_https} for follower in followers] 
    names = []
    for i,v in enumerate(profiles["followers"]):
        names.append(v['username'])
        
    links = []
    for i,v in enumerate(profiles["followers"]):
        links.append(v['photo'])
        
    get_images(names, links)
    header = Image.open("twitter-banner.png")
    user1 = Image.open(f'{names[0]}.jpg').resize((70,70),)
    user2 = Image.open(f'{names[1]}.jpg').resize((70,70),)
    user3 = Image.open(f'{names[2]}.jpg').resize((70,70),)
    get_image_header(header, user1, user2, user3)
    api.update_profile_banner('pasted-twitter-banner.png')
    print("Done updating banner!")



