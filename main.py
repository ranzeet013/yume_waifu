from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
import requests
from datetime import datetime
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

app = FastAPI()

sfw_genres = [
    'waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug',
    'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile',
    'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill',
    'kick', 'happy', 'wink', 'poke', 'dance', 'cringe'
]
nsfw_genres = ['waifu', 'neko', 'trap', 'blowjob']

# Ensure the "images" folder exists
if not os.path.exists("images"):
    os.makedirs("images")

def generate_waifu_image(genre, nsfw):
    try:
        endpoint = f'https://api.waifu.pics/{nsfw}/{genre}'
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        if 'url' not in data:
            raise HTTPException(status_code=404, detail="No image URL found.")

        waifu_url = data['url']
        response = requests.get(waifu_url)
        response.raise_for_status()


        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = f'images/{nsfw}_{genre}_{timestamp}.jpg'
        with open(file_path, 'wb') as f:
            f.write(response.content)

        return file_path, waifu_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

def create_prompt(nsfw):
    if nsfw == 'sfw':
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(
                    """You are a playful, friendly AI chatbot. Your tone is lighthearted, respectful, and fun, making sure to keep the conversation positive and engaging. You enjoy witty banter, clever jokes, and friendly compliments. Always maintain a warm, welcoming vibe, and never cross boundaries. You prioritize respectful interactions at all times."""
                )),
                HumanMessagePromptTemplate.from_template("{human_input}"),
            ]
        )
    elif nsfw == 'nsfw':
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(
                    """You are a playful AI chatbot with a flirty, cheeky tone. While being playful and engaging, you remain respectful, consensual, and avoid crossing any personal boundaries. Your goal is to make the conversation fun and light, with an emphasis on flirtatious banter while maintaining respect at all times."""
                )),
                HumanMessagePromptTemplate.from_template("{human_input}"),
            ]
        )
    return prompt

@app.get("/generate")
def generate_image(genre: str, nsfw: str = "sfw"):
    genres = sfw_genres if nsfw == "sfw" else nsfw_genres
    if genre not in genres:
        raise HTTPException(status_code=400, detail="Invalid genre selection.")


    file_path, waifu_url = generate_waifu_image(genre, nsfw)


    conversational_memory_length = 5
    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)


    groq_api_key = 'enter api key'
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name='llama3-8b-8192'
    )


    prompt = create_prompt(nsfw)


    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )

    if nsfw == "sfw":
        response = "Ah, looks like you're in the right place for some wholesome fun! 😄 I'm all about keeping things light and positive here. If you need any advice or ideas, feel free to ask"
    else:
        response = "Uh-oh, seems like you’re looking for something a little too wild! 😅 Let’s keep it fun and friendly here—no need to go down that path. But if you’ve got other questions, I’m all ears"


    return {
        "image_path": f"http://127.0.0.1:8000/images/{os.path.basename(file_path)}",
        "image_url": waifu_url,
        "chat_response": response,
    }

@app.get("/images/{image_name}")
def get_image(image_name: str):
    file_path = os.path.join("images", image_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found.")
    return FileResponse(file_path)
