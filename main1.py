from pydantic import BaseModel, ValidationError
from ollama import AsyncClient
import asyncio
import json


# Define the schema for the response
class FriendInfo(BaseModel):
    name: str
    age: int | None
    is_available: bool  # Required field


class FriendList(BaseModel):
    friends: list[FriendInfo]


async def main():
    client = AsyncClient()
    response = await client.chat(
        model='llama3.2',
        messages=[{
            'role': 'user',
            'content': ('''
                        "I have ten friends. The first is Alice, 25 years old and available for a chat anytime. The second is Bob, 30 years old and busy with work. The third is Charlie, 22 years old and planning a trip with me. The fourth is Diana, 27 years old and currently unavailable due to exams. The fifth is Ethan, 35 years old and eager to help me with a project. The sixth is Fiona, 29 years old and occupied with her art exhibit. The seventh is George, 31 years old and free to hang out this weekend. The eighth is Hannah, 24 years old and busy preparing for a marathon. The ninth is Ian, 28 years old and excited to go hiking with me. Finally, the tenth is Julia, 26 years old and always ready to lend a hand."
                "Return a list of friends in JSON format. Each friend should have a 'name', 'age', and 'is_available' field."
            '''
            )
        }],
        format="json",  # Specify format as 'json'
        options={'temperature': 0},  # Make responses more deterministic
    )

    try:
        # Parse the response into a dictionary
        response_data = json.loads(response.message.content)
        
        print("response_data: ", response_data)
        
        # Preprocess the response to ensure all fields are present
        for friend in response_data.get('friends', []):
            if 'is_available' not in friend:
                friend['is_available'] = False  # Default value if missing
                
            if 'age' not in friend:
                friend['age'] = None  # Default value if missing

        # Validate the processed response
        friends_response = FriendList.model_validate(response_data)
        print(f"\n{friends_response}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    except ValidationError as e:
        print("Validation errors:", e.json())


if __name__ == '__main__':
    asyncio.run(main())

