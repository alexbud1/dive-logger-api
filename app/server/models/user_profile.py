from server.database.database import database


class UserProfile:
    name: str
    is_diver: bool
    amount_of_dives: int = None
    country: str = None
    profile_photo: str = None

    def __init__(self, data_dict):
        self.name = data_dict.get("name")
        self.is_diver = data_dict.get("is_diver")
        self.amount_of_dives = data_dict.get("amount_of_dives", None)
        self.country = data_dict.get("country", None)
        self.profile_photo = data_dict.get("profile_photo", None)

    def __repr__(self):
        return f"<UserProfile {self.name}>"

    def to_json(self):
        return {
            "name": self.name,
            "is_diver": self.is_diver,
            "amount_of_dives": self.amount_of_dives,
            "country": self.country,
            "profile_photo": self.profile_photo,
        }

    async def save(self):
        await database.user_profiles.insert_one(self.to_json())
        return self
