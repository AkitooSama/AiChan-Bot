#Importing in-built modules.
from dataclasses import dataclass
from typing import Optional, Type, TypeVar
#Importing py-mongo module.
from pymongo.collection import Collection

@dataclass
class ChannelGreetings:
    """
    Represents a set of greetings for a channel.

    Attributes:
    - main_title (str): The main title of the greeting.
    - description (str): A brief description or content of the greeting.
    - rgb_color (tuple): RGB color values.
    - field (str): A field associated with the greeting.
    - footer_field (str): Footer field content.
    - thumbnail_url (str): (optional) URL for the thumbnail image.
    - image_url (str): URL for the main image.
    - footer_url (str): URL for the footer image.
    """
    main_title: Optional[str] = None
    description: Optional[str] = None
    rgb_color: Optional[tuple] = None
    field: Optional[str] = None
    field_description: Optional[str] = None
    footer_field: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    footer_url: Optional[str] = None
    
    
class WelcomeGreetingItems(ChannelGreetings):
    """Inherits from ChannelGreetings to represent welcome greeting items."""


class ExitGreetingItems(ChannelGreetings):
    """Inherits from ChannelGreetings to represent exit greeting items."""

    
class DmGreetingItems(ChannelGreetings):
    """Inherits from ChannelGreetings to represent dm greeting items."""

GreetingType = TypeVar("GreetingType", bound=ChannelGreetings)

class DatabaseInterface:
    @staticmethod
    def save_greeting_to_db(collection: Collection, greeting: GreetingType, greeting_type: str):
        # Convert greeting instance to a dictionary for MongoDB storage
        greeting_dict = greeting.__dict__
        
        # Save the greeting data to the database under the guild_id
        collection.update_one({'_id': greeting_type}, {f'$set': {f'{greeting_type}_data': greeting_dict}}, upsert=True)
    
    @staticmethod
    def get_greeting_from_db(collection: Collection, greeting_cls: Type[GreetingType], greeting_type: str) -> GreetingType:
        # Retrieve greeting data from the database based on guild_id
        data = collection.find_one({'_id': greeting_type})
        
        # Create a greeting instance from the retrieved data
        greeting = greeting_cls(**data.get(f'{greeting_type}_data')) if data else greeting_cls()
        return greeting
    
if __name__ == "__main__":
    pass