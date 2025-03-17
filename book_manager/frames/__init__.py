# Import all frames to make them available from the frames package
from book_manager.frames.home_frame import HomeFrame
from book_manager.frames.view_frame import ViewBooksFrame
from book_manager.frames.add_frame import AddBookFrame
from book_manager.frames.update_frame import UpdateBookFrame
from book_manager.frames.login_frame import LoginFrame
from book_manager.frames.homePage_frame import HomeFramePage

# Expose frame classes for direct import from frames package
__all__ = ['HomeFrame', 'ViewBooksFrame', 'AddBookFrame', 'UpdateBookFrame', 'LoginFrame', 'HomeFramePage']