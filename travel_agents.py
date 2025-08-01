from dotenv import load_dotenv
import os  # Load variables from .env file
from groq import Groq
load_dotenv()
client = Groq()
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
      {
        "role": "user",
        "content": "I NEED travel agent models to discuss each other based on user instructions. they give trip details overview and everything\n "
      },
      {
        "role": "assistant",
        "content": "Here are five travel agent models, each with their own unique characteristics and expertise. They'll discuss and provide trip details based on user instructions.\n\n**Travel Agent Models:**\n\n1. **Alex - The Adventure Expert**: Specializes in outdoor activities, trekking, and adventure travel.\n2. **Samantha - The Luxury Traveler**: Focuses on high-end travel, luxury resorts, and exclusive experiences.\n3. **Jack - The Budget Explorer**: Expertise in affordable travel, backpacking, and budget-friendly destinations.\n4. **Ramesh - The Cultural Connoisseur**: Knowledgeable about cultural heritage sites, historical landmarks, and local experiences.\n5. **Emily - The Family Traveler**: Specializes in family-friendly travel, kid-friendly activities, and group tours.\n\n**User Instruction:**\n\nLet's say a user instructs: \"I'm planning a 7-day trip to Japan. I'm interested in exploring Tokyo, Kyoto, and Osaka. I have a moderate budget and prefer cultural experiences. Which travel agent model would you recommend, and what itinerary would they suggest?\"\n\n**Discussion among Travel Agent Models:**\n\n**Alex (The Adventure Expert)**: \"Hey team, I'm not the best fit for this trip, as Japan has limited adventure activities. However, I can suggest some outdoor activities like hiking in Nikko or visiting the Japanese Alps. Samantha, you're more familiar with luxury travel; perhaps you can help with high-end options in Tokyo?\"\n\n**Samantha (The Luxury Traveler)**: \"Thanks, Alex. While I can offer luxurious accommodations in Tokyo, I think Ramesh might be a better fit for this trip. He's knowledgeable about cultural heritage sites in Japan. Ramesh, can you help with a cultural-focused itinerary?\"\n\n**Ramesh (The Cultural Connoisseur)**: \"Ah, perfect! Japan is a treasure trove of cultural experiences. For a 7-day trip, I'd suggest visiting Tokyo's Meiji Shrine, Kyoto's Fushimi Inari Shrine, and Osaka's Osaka Castle. I'd also recommend exploring traditional Japanese gardens, temples, and trying local cuisine like sushi and ramen.\"\n\n**Jack (The Budget Explorer)**: \"Hold on, Ramesh, I think I can help with budget-friendly options. Instead of staying in luxury hotels, we could opt for affordable guesthouses or hostels. I can suggest some budget-friendly areas to stay in Tokyo, Kyoto, and Osaka.\"\n\n**Emily (The Family Traveler)**: \"I'm not sure about this trip, as it seems more geared towards adults. However, I can offer some insights on family-friendly activities in Tokyo, like visiting the Tokyo Disneyland or the Ghibli Museum. Perhaps we can incorporate some kid-friendly activities into the itinerary?\"\n\n**Ramesh (The Cultural Connoisseur)**: \"Great suggestions, team! Based on our discussion, I'd propose a 7-day itinerary:\n\nDay 1: Arrival in Tokyo, visit the Meiji Shrine, and explore Shinjuku Gyoen National Garden.\n\nDay 2: Tokyo - Visit the Tokyo National Museum, Asakusa Kannon Temple, and enjoy a traditional Japanese dinner.\n\nDay 3: Travel to Kyoto, visit the Fushimi Inari Shrine, and stroll through Gion district.\n\nDay 4: Kyoto - Explore Kinkaku-ji Temple (Golden Pavilion), Arashiyama Bamboo Grove, and enjoy a traditional tea ceremony.\n\nDay 5: Travel to Osaka, visit Osaka Castle, and explore the Dotonbori area.\n\nDay 6: Osaka - Visit the Umeda Sky Building, Osaka Aquarium Kaiyukan, and try some local street food.\n\nDay 7: Departure from Osaka.\n\n**Samantha (The Luxury Traveler)**: \"Ramesh, that sounds like a great itinerary. I can add some luxury touches, like booking a high-end hotel in Tokyo and a traditional ryokan in Kyoto.\"\n\n**Jack (The Budget Explorer)**: \"I can offer some budget-friendly alternatives for accommodations and transportation.\"\n\n**Alex (The Adventure Expert)**: \"While I'm not directly involved, I'm happy to provide some outdoor activity suggestions for the itinerary.\"\n\n**Emily (The Family Traveler)**: \"I can help with kid-friendly activities and family-friendly accommodations, if needed.\"\n\nThe travel agent models have discussed and provided a comprehensive trip overview, including cultural experiences, luxury options, budget-friendly alternatives, and family-friendly activities. The user can now choose the best travel agent model and itinerary based on their preferences."
      },
      {
        "role": "user",
        "content": ""
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
