from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

client = OpenAI()
response = client.responses.create(
    model="gpt-5-nano",
    instructions="Говори, как будто бы тот, кто задает тебе вопрос умственно отсталый. Отвечай просто и понятно. И сильно груби",
    input="Что такое питон"
)
# 
print(response.output_text)