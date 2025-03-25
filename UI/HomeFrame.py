import tkinter as tk
import customtkinter as ctk
import os
import sys
from PIL import Image, ImageTk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Moduls.Home import HomeManager

class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.home_manager = HomeManager()
        self.configure(fg_color="#1E1E1E", corner_radius=0)
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top panel with header and user info
        self.create_top_panel(main_container)
        
        # Center content with featured books carousel and navigation buttons
        self.create_center_content(main_container)
        
        # Footer with additional info
        self.create_footer(main_container)
    
    def create_top_panel(self, parent):
        # Top panel
        top_panel = ctk.CTkFrame(parent, fg_color="#222222", corner_radius=10, height=100)
        top_panel.pack(fill="x", pady=(0, 20))
        top_panel.pack_propagate(False)  # Don't shrink to children size
        
        # Logo and app name on left
        logo_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        logo_frame.pack(side="left", padx=20)
        
        # Try to load logo
        try:
            logo_path = self.home_manager.get_asset_path("logo_small.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((40, 40))
            self.logo_photo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(40, 40))
            
            logo_label = ctk.CTkLabel(logo_frame, image=self.logo_photo, text="")
            logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        app_name = ctk.CTkLabel(
            logo_frame,
            text="BOOK-KU",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            text_color="#FFFFFF"
        )
        app_name.pack(side="left")
        
        # Time and user info on right
        info_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        info_frame.pack(side="right", padx=20)
        
        # Current date/time
        date_label = ctk.CTkLabel(
            info_frame,
            text=self.home_manager.get_current_date(),
            font=ctk.CTkFont(family="Arial", size=14),
            text_color="#AAAAAA"
        )
        date_label.pack(side="top", anchor="e")
        
        # Current user
        user_info = self.home_manager.get_user_info(self.controller.current_user)
        user_text = f"Welcome, {user_info['name']}"
        user_label = ctk.CTkLabel(
            info_frame,
            text=user_text,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        user_label.pack(side="top", anchor="e")
        
        # Profile and logout buttons
        button_frame = ctk.CTkFrame(top_panel, fg_color="transparent")
        button_frame.pack(side="right", padx=(0, 20))
        
        logout_btn = ctk.CTkButton(
            button_frame,
            text="Logout",
            font=ctk.CTkFont(family="Arial", size=14),
            fg_color="#4d6980",
            hover_color="#3c5b74",
            corner_radius=8,
            width=100,
            height=30,
            command=self.logout
        )
        logout_btn.pack(side="right", padx=(10, 0))
    
    def create_center_content(self, parent):
        # Center content
        center_content = ctk.CTkFrame(parent, fg_color="transparent")
        center_content.pack(fill="both", expand=True)
        
        # Layout for center content
        center_content.columnconfigure(0, weight=1)
        center_content.rowconfigure(0, weight=1)  # Banner
        center_content.rowconfigure(1, weight=2)  # Navigation buttons
        
        # Banner frame
        banner_frame = ctk.CTkFrame(center_content, fg_color="#2B2B2B", corner_radius=15)
        banner_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        # Create a nice banner with featured books
        self.create_banner(banner_frame)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(center_content, fg_color="transparent")
        nav_frame.grid(row=1, column=0, sticky="nsew")
        
        # Create navigation buttons based on user role
        self.create_navigation_buttons(nav_frame)
    
    def create_banner(self, parent):
        # Try to load banner image
        try:
            banner_path = self.home_manager.get_asset_path("banner.jpg")
            banner_img = Image.open(banner_path)
            banner_img = banner_img.resize((980, 200))
            self.banner_photo = ctk.CTkImage(light_image=banner_img, dark_image=banner_img, size=(980, 200))
            
            banner_label = ctk.CTkLabel(parent, image=self.banner_photo, text="")
            banner_label.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error loading banner: {e}")
            
            # Fallback if image loading fails
            fallback_frame = ctk.CTkFrame(parent, fg_color="#232F3E", corner_radius=0)
            fallback_frame.pack(fill="both", expand=True)
            
            welcome_label = ctk.CTkLabel(
                fallback_frame,
                text="Welcome to BOOK-KU",
                font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
                text_color="#FFFFFF"
            )
            welcome_label.place(relx=0.5, rely=0.4, anchor="center")
            
            subtitle_label = ctk.CTkLabel(
                fallback_frame,
                text="Your Digital Library Experience",
                font=ctk.CTkFont(family="Arial", size=18),
                text_color="#AAAAAA"
            )
            subtitle_label.place(relx=0.5, rely=0.6, anchor="center")
    
    def create_navigation_buttons(self, parent):
        # Container for 3 main buttons
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack(fill="both", expand=True)
        
        # Configure grid for equal spacing
        button_container.columnconfigure(0, weight=1)
        button_container.columnconfigure(1, weight=1)
        button_container.columnconfigure(2, weight=1)
        button_container.rowconfigure(0, weight=1)
        
        # Get button configuration based on role
        user_info = self.home_manager.get_user_info(self.controller.current_user)
        print(self.controller.current_user)
        print(user_info["role"])
        button_config = self.home_manager.get_navigation_config(user_info["role"])
        
        # Create the buttons
        for i, config in enumerate(button_config):
            self.create_nav_button(
                button_container, 
                config["text"], 
                config["icon"], 
                config["frame"], 
                config["color"], 
                i
            )
    
    def create_nav_button(self, parent, text, icon_file, target_frame, color, position):
        # Button frame
        button_frame = ctk.CTkFrame(parent, fg_color=color, corner_radius=15)
        button_frame.grid(row=0, column=position, padx=15, sticky="nsew")
        
        # Make button clickable
        button_frame.bind("<Button-1>", lambda e, frame=target_frame: self.controller.showFrame(frame))
        
        # Button container for proper layout
        content_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)
        
        # Try to load icon
        try:
            icon_path = self.home_manager.get_asset_path(icon_file)
            if os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((64, 64))
                icon_photo = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(64, 64))
                
                icon_label = ctk.CTkLabel(content_frame, image=icon_photo, text="")
                icon_label.image = icon_photo  # Keep reference
                icon_label.pack(pady=(20, 10))
            else:
                # If icon file doesn't exist, create placeholder
                placeholder = ctk.CTkLabel(
                    content_frame,
                    text="📚",
                    font=ctk.CTkFont(size=48),
                    text_color="#FFFFFF"
                )
                placeholder.pack(pady=(20, 10))
        except Exception as e:
            print(f"Error loading icon {icon_file}: {e}")
            # Fallback if icon loading fails
            placeholder = ctk.CTkLabel(
                content_frame,
                text="📚",
                font=ctk.CTkFont(size=48),
                text_color="#FFFFFF"
            )
            placeholder.pack(pady=(20, 10))
        
        # Button text
        text_label = ctk.CTkLabel(
            content_frame,
            text=text,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color="#FFFFFF"
        )
        text_label.pack(pady=(10, 20))
        
        # Add hover effect
        for widget in [button_frame, content_frame, text_label]:
            widget.bind("<Enter>", lambda e, bf=button_frame, c=color: self.on_button_hover(bf, c))
            widget.bind("<Leave>", lambda e, bf=button_frame, c=color: self.on_button_leave(bf, c))
            widget.bind("<Button-1>", lambda e, frame=target_frame: self.controller.showFrame(frame))
    
    def on_button_hover(self, button, original_color):
        # Darken the color on hover
        darker = self.home_manager.adjust_color(original_color)
        button.configure(fg_color=darker)
    
    def on_button_leave(self, button, original_color):
        # Restore original color
        button.configure(fg_color=original_color)
    
    def create_footer(self, parent):
        # Footer
        footer = ctk.CTkFrame(parent, fg_color="#222222", corner_radius=10, height=50)
        footer.pack(fill="x", pady=(20, 0))
        footer.pack_propagate(False)  # Don't shrink to children size
        
        # Copyright text
        copyright_label = ctk.CTkLabel(
            footer,
            text=self.home_manager.get_copyright_text(),
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA"
        )
        copyright_label.pack(side="left", padx=20, pady=10)
        
        # Version info
        version_label = ctk.CTkLabel(
            footer,
            text="Version 1.0",
            font=ctk.CTkFont(family="Arial", size=12),
            text_color="#AAAAAA"
        )
        version_label.pack(side="right", padx=20, pady=10)
    
    def logout(self):
        """Handle logout"""
        if hasattr(self.controller, 'current_user'):
            self.controller.current_user = None
        
        self.controller.showFrame("LoginFrame")


# For testing purposes
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1024x768")
    root.title("Home Test")
    
    class MockController:
        def __init__(self):
            self.current_user = {"username": "admin", "role": "admin"}
            
        def showFrame(self, frame_name):
            print(f"Showing frame: {frame_name}")
    
    frame = HomeFrame(root, MockController())
    frame.pack(fill="both", expand=True)
    
    root.mainloop()