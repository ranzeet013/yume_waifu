# Yume Waifus

Yume Waifus is an API-based web application built using **FastAPI** that allows users to generate waifu (anime-inspired character) images and interact with a playful, conversational AI chatbot. The primary purpose of the app is to provide users with both a fun visual experience and engaging chatbot responses. 

**Disclaimer**: I was really bored and didn’t know what to do, so I landed on this project. Don’t judge, it's a fun little thing, and I just went with it. 😅

## Key Features of Yume Waifus

### Waifu Image Generation:
- The app can generate waifu images based on different genres, letting users select either safe-for-work (SFW) or not-safe-for-work (NSFW) content.
- It uses an external API ([Waifu.pics](https://api.waifu.pics)) to fetch waifu images. Depending on the genre selected by the user, it makes a request to the corresponding API endpoint to retrieve an image.
- The images are saved locally with a timestamp in the "images" folder. The app returns the image path (viewable through a local web server) and the image URL.
- Genres include SFW genres like waifu, neko, hug, kiss, smile, etc., and NSFW genres like trap, blowjob, etc. (Don’t say I didn’t warn you!)

### Chatbot Interaction:
- The app includes a conversational AI chatbot that responds based on the genre selected (SFW or NSFW).
- The chatbot’s tone and style change depending on the `nsfw` parameter:
  - **SFW (Safe for Work)**: The chatbot keeps things friendly, playful, and positive, making sure all interactions are fun and respectful.
  - **NSFW (Not Safe for Work)**: The chatbot gets a little cheeky but still keeps it lighthearted and respectful, sticking to the whole consensual vibe. 
- **Langchain** is used to manage conversation memory and maintain dynamic dialogue. It also interacts with **Groq**, an AI model (presumably Llama 3-8b), to generate the chatbot’s responses. The memory of past conversations is retained for up to 5 exchanges.

### Dynamic Prompt Creation:
- The chatbot’s behavior is affected by the `nsfw` parameter, creating different prompts based on whether the user is after SFW or NSFW content.
- The system message helps set the tone — friendly and respectful for SFW, flirtatious for NSFW, keeping it fun for both!

### File and Image Handling:
- The app checks if the "images" folder exists and creates it if needed (no missing files here).
- Images are saved locally in the "images" folder, and users can retrieve these images through the `/images/{image_name}` endpoint.
- The app returns the image path in the response, which is a URL pointing to the image location on the local server.

## Application Structure

### FastAPI Routes:
- `/generate`: This is the main endpoint for generating the waifu image and fetching the chatbot's response. It accepts `genre` (e.g., "waifu", "neko") and `nsfw` (either "sfw" or "nsfw") as query parameters. The endpoint calls `generate_waifu_image` to get the image, saves it locally, and invokes the chatbot to return a response.
- `/images/{image_name}`: This endpoint serves the generated image. It checks if the requested image exists in the "images" folder and returns the image using **FileResponse**. If the image is missing, it raises a 404 error.

## Technical Components:
- **FastAPI**: The backend framework that handles HTTP requests and serves images.
- **Requests**: Used for making HTTP requests to fetch images from the waifu API.
- **Langchain**: Manages language models and conversation memory, integrating the chatbot that communicates with **Groq** to generate responses.
- **Groq**: An AI model used for generating chatbot responses, initialized with the API key and model name ('llama3-8b-8192').
- **Datetime**: Used for timestamping image files to prevent naming conflicts.
- **OS**: Handles directory creation, file paths, and checks if files are in the right place.

## Example Flow:
1. A user sends a GET request to `/generate` with parameters like `genre=waifu` and `nsfw=sfw`.
2. The server fetches the corresponding waifu image from the external API, saves it locally, and generates a playful chatbot response based on the SFW prompt.
3. The server returns the image URL and the chatbot response back to the user.

## Overall Project Purpose:
**Yume Waifus** is designed to provide an interactive, fun, and lighthearted experience. It combines anime-inspired visuals with an AI chatbot, allowing users to enjoy both playful images and engaging conversations tailored to their preferences (whether SFW or NSFW). So if you're looking for something quirky and entertaining, this might be just the project for you!
