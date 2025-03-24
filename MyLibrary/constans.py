# constants.py

# Colors
COLOR_DARK = {
    "primary": "#4285F4",          # Google Blue - technology, clarity of thought
    "primaryVariant": "#1A73E8",   # Deeper Blue - trustworthiness and reliability
    "accent": "#00D4FF",           # Bright Cyan - innovation and creativity
    "accentVariant": "#00A8E8",    # Deep Cyan - depth of knowledge
    "background": "#1A1D2C",       # Dark Blue-Gray - intellectual space
    "surface": "#252A3D",          # Slate Blue - content foundation
    "inputField": "#2E3A59",       # Navy Blue - focused input areas
    "primaryText": "#E9ECEF",      # Off-White - clear readability
    "secondaryText": "#B0B7C3",    # Silver - supplementary information
    "highlight": "#6C63FF",        # Indigo - attention and innovation
    "cancelButton": "#FF5A5A",     # Coral Red - clear negative action
    "border": "#3A4257",           # Steel Blue - subtle separation
    "error": "#FF5A5A",            # Bright Red - error states
    "success": "#2DD4BF",          # Teal - positive outcomes
    "warning": "#FF9F45",          # Amber - cautionary notifications
    "disabled": "#4A5169",         # Slate Gray - inactive elements
    "hover": {
        "primary": "#5C9CFF",      # Lighter Blue - interactive elements
        "accent": "#33DDFF",       # Lighter Cyan - secondary interaction
        "button": "#3D4D77"        # Muted Blue - button hover state
    },
    "active": {
        "primary": "#0D47A1",      # Oxford Blue - active state
        "accent": "#00BFE6",       # Darker Cyan - pressed accent elements
        "button": "#1E263B"        # Deep Navy - button press state
    },
    "selected": "#323B54",         # Medium Blue - selected items
    "overlay": "rgba(13, 18, 30, 0.7)" # Transparent Dark Blue - modal overlays
}

COLOR_LIGHT = {
    "primary": "#3365FF",          # Deep Blue - intelligence and academic rigor
    "primaryVariant": "#2951CC",   # Oxford Blue - traditional academic excellence
    "accent": "#00A8E8",           # Teal - fresh thinking and intellectual innovation
    "accentVariant": "#0089BC",    # Deep Teal - sustainable knowledge
    "background": "#F5F7FA",       # Off-White - clean, scholarly environment
    "surface": "#FFFFFF",          # White - clarity of thought
    "inputField": "#EFF2F7",       # Platinum - subtle sophistication
    "primaryText": "#1A1D2C",      # Almost Black - authority and clarity
    "secondaryText": "#545B6B",    # Slate - nuanced thinking
    "highlight": "#6C63FF",        # Purple - insight and innovation
    "cancelButton": "#FF5A5A",     # Bright Red - clear action distinction
    "border": "#E2E8F0",           # Light Gray - delicate definition
    "error": "#D32F2F",            # Error state
    "success": "#0FC792",          # Success state
    "warning": "#FF9F45",          # Warning state
    "disabled": "#D1D5DB",         # Disabled state
    "hover": {
        "primary": "#4D7AFF",      # Lighter Blue - hover state
        "accent": "#33B7ED",       # Lighter Teal - accent hover
        "button": "#E8F0FE"        # Very Light Blue - button hover
    },
    "active": {
        "primary": "#1E4BD2",      # Darker Blue - pressed state
        "accent": "#0089BC",       # Darker Teal - accent pressed
        "button": "#D6E4FF"        # Light Blue - button press
    },
    "selected": "#EBF2FF",         # Very Light Blue - selected items
    "overlay": "rgba(244, 247, 252, 0.8)" # Transparent Light - modal overlays
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
