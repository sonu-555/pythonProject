import os
import logging
import whisper

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set directories
MEDIA_FOLDER = r"C:\Users\hp\Documents"  # Change if needed
OUTPUT_FOLDER = r"C:\music\transcriptions"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Whisper model
logging.info("Loading Whisper model...")
model = whisper.load_model("tiny")


def transcribe_file(file_path):
    """Transcribes a media file and saves the result as a text file."""
    try:
        logging.info(f"Transcribing: {file_path}")
        result = model.transcribe(file_path)
        text = result["text"].strip()

        if not text:
            logging.warning(f"Skipping empty transcription: {file_path}")
            return

        # Remove original extension before saving
        file_name = os.path.splitext(os.path.basename(file_path))[0] + ".txt"
        output_file = os.path.join(OUTPUT_FOLDER, file_name)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        logging.info(f"Saved transcription: {output_file}")
    except Exception as e:
        logging.error(f"Error transcribing {file_path}: {e}")


def main():
    """Finds media files (including subfolders) and transcribes them."""
    media_extensions = {'.mp3', '.wav', '.m4a', '.mp4', '.mkv'}

    # Recursively find all media files
    media_files = []
    for root, _, files in os.walk(MEDIA_FOLDER):
        for file in files:
            if file.lower().endswith(tuple(media_extensions)):
                media_files.append(os.path.join(root, file))

    if not media_files:
        logging.warning("No media files found in the directory.")
        return

    for file in media_files:
        transcribe_file(file)


if __name__ == "__main__":
    main()
