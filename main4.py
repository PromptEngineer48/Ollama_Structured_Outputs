from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]

while True:
    # Get the country name from the user
    user_country = input("Enter the name of the country you want information about (or type 'bye' to exit): ").strip()
    
    # Exit the loop if the user types 'bye'
    if user_country.lower() == "bye":
        print("Goodbye!")
        break

    # Fetch and display information about the country
    try:
        response = chat(
            messages=[
                {
                    'role': 'user',
                    'content': (
                        f"Provide information about {user_country} in the following JSON format: "
                        "{'name': <country_name>, 'capital': <capital>, 'languages': [<languages>]}"
                    ),
                }
            ],
            model='llama3.2',
            format='json',  # Ensure JSON response
        )

        # Validate and parse the response
        country = Country.model_validate_json(response.message.content)

        print(country)
        print("\n")
        
    except Exception as e:
        print("An error occurred:", e)
