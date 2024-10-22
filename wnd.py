import pygetwindow as gw
import pyautogui
import time


def click_window(title):
    try:
        print(gw.getWindowsWithTitle(title))
        # Get the window by its title
        window = gw.getWindowsWithTitle(title)[0]

        # Bring the window to the front
        # window.activate()

        # Wait for the window to be focused
        time.sleep(0.5)

        # Calculate the center of the window
        x, y = window.left + window.width // 2, window.top + window.height // 2

        # Move the mouse to the center of the window and click
        pyautogui.click(x, y)
        print(f"Clicked on window: {title}")

    except IndexError:
        print(f"No window with title '{title}' found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    window_title = input("Enter the title of the window you want to click: ")
    click_window(window_title)
