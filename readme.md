# Image to Text Processor with OpenAI Integration

This script monitors a specified folder for new image files, extracts text from these images using OCR (Optical Character Recognition) with Tesseract, and then generates responses using the OpenAI GPT-3.5-turbo model based on the extracted text.

## Features

- **Automatic Folder Monitoring**: Uses `watchdog` to watch for new image files in a specified folder.
- **OCR with Tesseract**: Extracts text from images using Tesseract.
- **OpenAI Integration**: Sends the extracted text to OpenAI's GPT-3.5-turbo model to generate responses.
- **Colored Console Output**: Provides visually distinct colored output in the console.

## Prerequisites

Before running this script, ensure you have the following installed:

- Python 3.6+
- Tesseract-OCR
- Required Python packages (listed in `requirements.txt`)

The script will assist you through the required packages installation and the Tesseract software installation; you just need to confirm the installation.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/BohBOhTN/bot_technique_index.git
   cd bot_technique_index
