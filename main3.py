from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]


response = chat(
    messages=[
        {
            'role': 'user',
            'content': (
                "Provide information about India in the following JSON format: "
                "{'name': <country_name>, 'capital': <capital>, 'languages': [<languages>]}"
            ),
        }
    ],
    model='llama3.2',
    format='json',  # Ensure JSON response
)


# Parse and validate the response using the Country model
try:
    country = Country.model_validate_json(response.message.content)
    print(country)
except Exception as e:
    print("An error occurred:", e)
