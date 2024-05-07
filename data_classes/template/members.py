from dataclasses import dataclass
from typing import Optional, Type, TypeVar
from pymongo.collection import Collection
from functions.templates_maker import ProfileTemplate

@dataclass
class MemberProfile:
    member_name: Optional[str] = None
    server_name: Optional[str] = None
    friends: Optional[list] = None
    best_friends: Optional[list] = None
    pronouns: Optional[str] = None
    message_count: Optional[int] = None
    behavior_percentage: Optional[str] = None
    member_details: Optional[str] = None
    extra_information: Optional[str] = None
    template: Optional[str] = None

Profile = TypeVar("Profile", bound=MemberProfile)

class DatabaseInterface:
    def __init__(self, collection: Collection):
        self.collection = collection

    def save_data_to_db(self, member_id: int, data: dict) -> None:
        query = {"_id": "member_profile"}  # Specify a common _id for all members
        update_query = {"$set": {f"members.{member_id}": data}}  # Store member data under a nested key 'members' with member_id as subfields
        
        self.collection.update_one(query, update_query, upsert=True)

    def get_specific_data(self, member_id: int, field_name: str):
        query = {"_id": "member_profile", f"members.{member_id}": {"$exists": True}}
        projection = {f"members.{member_id}.{field_name}": 1, "_id": 0}

        result = self.collection.find_one(query, projection)
        if result:
            return result.get(f"members.{member_id}.{field_name}")
        else:
            return None

    def update_member_field(self, member_id: int, field_name: str, new_value) -> None:
        query = {"_id": "member_profile"}
        update_query = {"$set": {f"members.{member_id}.{field_name}": new_value}}
        self.collection.update_one(query, update_query)

    def add_element_to_list_field(self, member_id: int, field_name: str, element) -> None:
        query = {"_id": "member_profile"}
        update_query = {"$addToSet": {f"members.{member_id}.{field_name}": element}}
        self.collection.update_one(query, update_query)

    def remove_element_from_list_field(self, member_id: int, field_name: str, element) -> None:
        query = {"_id": "member_profile"}
        update_query = {"$pull": {f"members.{member_id}.{field_name}": element}}
        self.collection.update_one(query, update_query)
        
    def get_profile(self, member_id: int) -> Type[Profile]:
        query = {"_id": "member_profile", f"members.{member_id}": {"$exists": True}}
        data = self.collection.find_one(query)
        
        if data:
            profile_data = data['members'][f'{member_id}']
            template = ProfileTemplate(**profile_data).member_profile_template()
            profile = MemberProfile(template=template, **profile_data)
            return profile
        else:
            return None
        
if __name__ == "__main__":
    pass