#Importing discord module.
import discord
from setup import db  # Importing database.

async def get_specific_value_db(member: discord.Member, key: str, default_value: str = "general") -> str:
    """Fetches a specific value for a member's guild from the database.

    Parameters
    ----------
    member : discord.Member
        The Discord member object whose guild's value is being retrieved.
    key : str
        The key for the specific value to be fetched from the database.
    default_value : str, optional
        The default value to be used if the specified key is not found, by default "general".

    Returns
    -------
    str
        The value associated with the specified key for the member's guild. Defaults to the default_value if not found.
    """
    guild_collection = db[f"guild-{member.guild.id}"]  # Accessing the collection in the database based on guild ID.
    value_data = guild_collection.find_one(
        {key: {"$exists": True}},
        projection={"_id": 0, key: 1}  # Fetch only the specified key
    )

    if value_data:
        return value_data.get(key)

    # If the specified key is not found, create and store the default value for that key
    guild_collection.insert_one({key: default_value})
    return default_value

async def change_key_value_db(member: discord.Member, key: str, new_value: str) -> None:
    """
    Updates a specific key's value in the guild's database collection.

    This function takes a Discord member object, a key, and a new value
    to update a specific key-value pair within the guild's database collection.

    Parameters:
    - member (discord.Member): The Discord member object representing the user.
    - key (str): The key in the database collection to be updated.
    - new_value (str): The new value to update for the specified key.

    Notes:
    - Uses PyMongo's `update_one()` method to update a single document that matches
      the specified condition (key exists).
    - The function modifies the document in the guild's collection by setting the
      provided key to the new value.
    """
    guild_collection = db[f"guild-{member.guild.id}"]

    # Update a single document that matches the condition
    guild_collection.update_one(
        {key: {"$exists": True}},  # Specify the condition for finding the document
        {"$set": {key: new_value}},  # Update the key with the new value
        upsert=True
    )


async def save_to_db(guild_id: int, data: dict, data_type: str, replace: bool = False) -> None:
    """Saves or updates data in the database based on specified parameters.

    This method allows saving or updating data in a MongoDB collection associated with the given 'guild_id'.
    It performs different operations based on the 'replace' parameter:
    - If 'replace' is True, it completely replaces the data for the provided 'data_type'.
    - If 'replace' is False, it updates specific keys within the nested data object.

    Parameters
    ----------
    guild_id : int
        The identifier for the guild/server in the database.

    data : dict
        A dictionary containing the data to be saved or updated.

    data_type : str
        Specifies the type of data to save/update.

    replace : bool, optional
        If True, replaces the entire data for the given 'data_type'.
        If False, updates specific keys within the nested data object.
        Default is False.

    Note
    ----
    For 'replace=False', 'data' should contain the key-value pairs to update within the existing data.
    """
    collection = db[f"guild-{guild_id}"]
    
    if replace:
        # Completely replace the data for the given data_type
        collection.replace_one({'_id': data_type}, {'_id': data_type, f'{data_type}_data': data}, upsert=True)
    else:
        # Update specific keys within the nested data object
        update_query = {'_id': data_type}
        update_data = {f'$set': {f'{data_type}_data.{key}': value for key, value in data.items()}}
        collection.update_one(update_query, update_data, upsert=True)


async def get_from_db(guild_id: int, data_type: str) -> list:
    """Retrieves data from the database based on specified parameters.

    This method retrieves data from a MongoDB collection associated with the given 'guild_id'
    and specified 'data_type'. It finds the data based on the provided identifier ('_id').

    Parameters
    ----------
    guild_id : int
        The identifier for the guild/server in the database.

    data_type : str
        Specifies the type of data to retrieve.

    Returns
    -------
    list
        A list containing the retrieved data or an empty list if no data is found.

    Note
    ----
    The 'data_type' parameter specifies the type of data to fetch from the database.
    """
    collection = db[f"guild-{guild_id}"]
    
    # Retrieve greeting data from the database based on guild_id
    data = collection.find_one({'_id': data_type})
    
    # retrieving data
    data = data.get(f'{data_type}_data')
    return data

if __name__ == "__main__":
    pass