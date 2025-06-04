import cloudinary
from dotenv import load_dotenv
import os

load_dotenv()

print("Configuring Cloudinary...", os.getenv('CLOUDINARY_NAME'), "\n", os.getenv('CLOUDINARY_API_KEY'), "\n", os.getenv('CLOUDINARY_API_SECRET'))

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)
