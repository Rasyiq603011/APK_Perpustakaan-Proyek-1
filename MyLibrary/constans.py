# constants.py

# Colors
COLORS = {
    "primary": "#1a73e8",
    "secondary": "#34a853",
    "accent": "#fbbc05",
    "error": "#ea4335",
    "background": "#ffffff",
    "text": "#202124",
    "light_gray": "#f1f3f4",
    "dark_gray": "#5f6368"
}

# Fonts
FONTS = {
    "heading": "Roboto, sans-serif",
    "body": "Open Sans, sans-serif",
    "monospace": "Courier New, monospace"
}

# Text sizes
TEXT_SIZES = {
    "xs": "12px",
    "sm": "14px",
    "md": "16px",
    "lg": "18px",
    "xl": "24px",
    "xxl": "32px"
}

# Spacing
SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "xxl": "48px"
}

# Other UI constants
BORDER_RADIUS = "4px"
BOX_SHADOW = "0 2px 4px rgba(0, 0, 0, 0.1)"
TRANSITION = "all 0.3s ease"

# GENRE FOR FILTER
CATEGORY_MAPPING = {
    "Science Fiction": ["Science fiction", "Science fiction, American", "Science fiction, English",
                        "Interplanetary voyages", "Robots"],
    "Young Adult": ["Juvenile Fiction", "Young Adult Fiction", "Young adult fiction", "Fiksi Remaja"],
    "Graphic Novels": ["Graphic novel", "Graphic novels", "COMICS & GRAPHIC NOVELS", "Comic books, strips, etc",
                       "Horror comic books, strips, etc"],
    "Fiction": ["American fiction", "English fiction", "Fantasy fiction", "Historical fiction", "Adventure stories",
                "Romantic suspense fiction", "Detective and mystery stories", "Detective and mystery stories, English"],
    "Non-Fiction": ["Biography & Autobiography", "History", "Political Science", "Science", "Medical", "Psychology",
                    "Philosophy", "Self-Help", "True Crime"],
    "Education": ["Mathematics", "Literature", "Language Arts & Disciplines", "Study Aids", "Foreign Language Study"],
    "Arts & Humanities": ["ART", "Architecture", "Aesthetics", "Music", "Performing Arts", "Photography", "Design"],
    "Religion & Spirituality": ["Christian ethics", "Christian life", "Islam", "Islam and civilization", "Hadith",
                                "Faith"],
    "Social Sciences": ["Political leadership", "Sociology", "Anthropology", "Equality", "Ethics", "Economics",
                        "Business & Economics", "Law", "International relations"],
    "Nature & Environment": ["Nature", "Nature photography", "Climatic changes", "Wetland animals", "Agriculture",
                             "Animals", "Birds"],
}
