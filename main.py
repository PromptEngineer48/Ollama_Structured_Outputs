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
            'content': (
                "I have two friends. The first is Ollama, 29 years old and busy saving the world, "
                "and the second is Alonso, 23 years old and wants to hang out with me. "
                "Return a list of friends in JSON format. Each friend should have a 'name', 'age', and 'is_available' field."
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
            if 'availability' in friend:
                friend['is_available'] = friend.pop('availability')
            if 'is_available' not in friend:
                friend['is_available'] = False  # Default value if missing

        # Validate the processed response
        friends_response = FriendList.model_validate(response_data)
        print(friends_response)
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    except ValidationError as e:
        print("Validation errors:", e.json())


if __name__ == '__main__':
    asyncio.run(main())

