import tkinter as tk
import os
from views.main_view import MainView

def create_required_folders():
    """Create required folders if they don't exist"""
    folders = [
        "data",
        "assets",
        "assets/images"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def check_default_image():
    """Create a default book image if it doesn't exist"""
    default_image_path = "assets/images/default.jpeg"
    
    if not os.path.exists(default_image_path):
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a blank image
        img = Image.new('RGB', (100, 150), color = (200, 200, 200))
        draw = ImageDraw.Draw(img)
        
        # Try to add text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
            draw.text((20, 65), "BOOK", fill=(50, 50, 50), font=font)
        except:
            # If font not available, use simple text
            draw.text((20, 65), "BOOK", fill=(50, 50, 50))
        
        # Save the image
        img.save(default_image_path)

def main():
    """Main application entry point"""
    # Create required folders
    create_required_folders()
    
    # Check default image
    check_default_image()
    
    # Create the root window
    root = tk.Tk()
    
    # Initialize main view
    app = MainView(root)
    
    # Run the application
    app.run()

if __name__ == "__main__":
    main()
