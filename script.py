import pytesseract
from PIL import Image, UnidentifiedImageError
import re
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the colored library for text colorization
from colored import fg, attr

# Import OpenAI client
import openai
openai.api_key = 'sk-proj-p68xqKwS8GE2fzb3lWSCT3BlbkFJ66F8AUZJn2RMOQEe2DGU'

# Track processed files
processed_files = {}

def extract_text_from_image(image_path):
    for _ in range(10):  # Retry up to 10 times
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='fra')
            return text
        except PermissionError:
            time.sleep(0.5)  # Wait for half a second before retrying
        except UnidentifiedImageError:
            raise UnidentifiedImageError(f"Cannot identify image file: {image_path}")
    raise PermissionError(f"Failed to open image file: {image_path}")

def process_image(image_path):
    try:
        extracted_text = extract_text_from_image(image_path)
        response = generate_response(extracted_text)
        print(f"\n{fg('cyan')}Response from OpenAI:{attr(0)}\n{response}")
        print("--------------------")  # Print dashes to separate images
    except Exception as e:
        print(f"{fg('red')}Failed to process image {image_path}: {e}{attr(0)}")

def generate_response(extracted_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"lire puis répondre aux questions en se basant sur les choix donnés sans donner des explications : {extracted_text}"
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if response.choices:
        choice = response.choices[0]
        if 'message' in choice and 'content' in choice.message:
            return choice.message['content']
    return "No response from OpenAI"

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.png', '.jpg', '.jpeg')):
            print(f"\n{fg('yellow')}New image detected: {event.src_path}{attr(0)}")
            # Wait a bit to ensure the file is fully written
            time.sleep(2)
            
            # Check if the file has been processed recently
            if event.src_path in processed_files:
                if time.time() - processed_files[event.src_path] < 10:
                    return  # Skip processing if it was processed in the last 10 seconds
            
            try:
                process_image(event.src_path)
                processed_files[event.src_path] = time.time()
            except Exception as e:
                print(f"{fg('red')}Failed to process image {event.src_path}: {e}{attr(0)}")

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
