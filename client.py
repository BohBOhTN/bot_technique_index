import requests
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colored import fg, attr

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            print(f"\n{fg('yellow')}New image detected: {event.src_path}{attr(0)}")
            # Wait a bit to ensure the file is fully written
            time.sleep(2)
            try:
                response = process_image(event.src_path)
                print(f"\n{fg('cyan')}Response from API:{attr(0)}\n{response}")
                print("--------------------")  # Print dashes to separate images
            except Exception as e:
                print(f"{fg('red')}Failed to process image {event.src_path}: {e}{attr(0)}")

def process_image(image_path):
    url = 'http://127.0.0.1:5000/process-image'
    with open(image_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json().get('response', 'No response from API')
    else:
        raise Exception(response.json().get('error', 'Unknown error'))

def main():
    screenshots_folder = os.path.join(os.getcwd(), 'screenshots')
    os.makedirs(screenshots_folder, exist_ok=True)

    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=screenshots_folder, recursive=False)

    print(f"{fg('green')}Watching folder: {screenshots_folder}{attr(0)}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
