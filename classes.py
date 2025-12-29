import random
import json



def chance(percent: int):
    return random.random() < percent / 100

class Box:
    LUCKY_MULTIPLIERS = [0.5, 0.75, 1, 1.5, 2, 2.5, 3, 4]
    BOXES = {
        "basic": {
            "price": 50,
            "description": "A standard box with normal odds",
            "cat_count": 1,
            "weight_multipliers": {},
            "min_fluffy": 0,
            "max_fluffy": 100,
            "min_cute": 0,
            "max_cute": 100,
            "guaranteed_rarity": None,
            "is_lucky": False
        },
        "premium": {
            "price": 200,
            "description": "Better odds for rare cats",
            "cat_count": 1,
            "weight_multipliers": {
                "fur_color": {"rare": 2, "epic": 2, "legendary": 2, "mythic": 2},
                "eye_color": {"rare": 2, "epic": 2, "legendary": 2, "mythic": 2},
                "pattern": {"rare": 2, "epic": 2, "legendary": 2, "mythic": 2},
                "size": {"rare": 2, "epic": 2, "legendary": 2, "mythic": 2},
                "mood": {"rare": 2, "epic": 2, "legendary": 2, "mythic": 2},
                "breed": {"rare": 2, "epic": 2, "legendary": 2, "mythic": 2}
            },
            "min_fluffy": 0,
            "max_fluffy": 100,
            "min_cute": 0,
            "max_cute": 100,
            "guaranteed_rarity": None,
            "is_lucky": False
        },
        "fluffy": {
            "price": 150,
            "description": "Guaranteed fluffy and cute cats",
            "cat_count": 1,
            "weight_multipliers": {},
            "min_fluffy": 70,
            "max_fluffy": 100,
            "min_cute": 50,
            "max_cute": 100,
            "guaranteed_rarity": None,
            "is_lucky": False
        },
        "lucky": {
            "price": 300,
            "description": "Random odds - could be amazing or terrible",
            "cat_count": 1,
            "weight_multipliers": {},  # Generated randomly at unbox time
            "min_fluffy": 0,
            "max_fluffy": 100,
            "min_cute": 0,
            "max_cute": 100,
            "guaranteed_rarity": None,
            "is_lucky": True
        },
        "triple": {
            "price": 400,
            "description": "Three cats with lower stats",
            "cat_count": 3,
            "weight_multipliers": {
                "fur_color": {"rare": 0.5, "epic": 0.5, "legendary": 0.5, "mythic": 0.5},
                "eye_color": {"rare": 0.5, "epic": 0.5, "legendary": 0.5, "mythic": 0.5},
                "pattern": {"rare": 0.5, "epic": 0.5, "legendary": 0.5, "mythic": 0.5},
                "size": {"rare": 0.5, "epic": 0.5, "legendary": 0.5, "mythic": 0.5},
                "mood": {"rare": 0.5, "epic": 0.5, "legendary": 0.5, "mythic": 0.5},
                "breed": {"rare": 0.5, "epic": 0.5, "legendary": 0.5, "mythic": 0.5}
            },
            "min_fluffy": 0,
            "max_fluffy": 50,
            "min_cute": 0,
            "max_cute": 50,
            "guaranteed_rarity": None,
            "is_lucky": False
        }
    }
    @classmethod
    def get_box(cls, box_type):
        return cls.BOXES.get(box_type)
    
    @classmethod
    def get_price(cls, box_type):
        """Returns box price."""
        box = cls.get_box(box_type)
        return box["price"] if box else None
    
    @classmethod
    def get_weights(cls, box_type, attribute):
        
        box = cls.get_box(box_type)
        if not box:
            raise ValueError("Invalid box type")
        weights = Cat.RARITY_WEIGHTS.copy()
        
        if box["is_lucky"]:
            multiplier = random.choice(cls.LUCKY_MULTIPLIERS)
            for rarity in ["rare", "epic", "legendary", "mythic"]:
                weights[rarity] = int(weights[rarity] * multiplier)
        else:
            # Apply box multipliers
            if attribute in box["weight_multipliers"]:
                for rarity, mult in box["weight_multipliers"][attribute].items():
                    weights[rarity] = int(weights[rarity] * mult)
        
        return weights

    @classmethod
    def list_boxes(cls):
        print("\n📦 AVAILABLE BOXES 📦")
        print("━" * 30)
        for name, data in cls.BOXES.items():
            print(f"{name.upper()}: {data['price']} coins")
            print(f"  {data['description']}")
            print()

class Shop:
# In Shop class
    @staticmethod
    def buy_box(player, box_type):
        box = Box.get_box(box_type)
        if not box:
            raise ValueError(f"Invalid box type: {box_type}")
        box_cost = box["price"]
        if player.coins >= box_cost:
            player.coins -= box_cost
            cats = []
            for _ in range(box["cat_count"]):
                cat = Cat.unbox_cat(box_type)
                player.add_cat(cat)
                cats.append(cat)
            return cats
        else:
            raise ValueError(f"Not enough coins for {box_type} box.")

    @staticmethod
    def display_shop():
        print("\n🏪 CAT BOX SHOP 🏪")
        print("━" * 35)
        for name, data in Box.BOXES.items():
            cat_text = "cat" if data["cat_count"] == 1 else "cats"
            print(f"  {name.upper()} - {data['price']} coins ({data['cat_count']} {cat_text})")
            print(f"    {data['description']}")
        print("━" * 35)

class Cat:
    # Load attributes data with proper error handling
    try:
        with open("cat_attributes.json", "r") as file:
            ATTRIBUTES_DATA = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Critical error: cat_attributes.json not found. The game cannot start without this file.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Critical error: cat_attributes.json is corrupted or invalid JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error loading cat_attributes.json: {e}")
    RARITY_WEIGHTS = {
    "common": 100,
    "uncommon": 50,
    "rare": 20,
    "epic": 8,
    "legendary": 3,
    "mythic": 1
}
    RARITY_POINTS = {
    "common": 1,
    "uncommon": 3,
    "rare": 10,
    "epic": 30,
    "legendary": 100,
    "mythic": 500
}
    RARITY_THRESHOLDS = [
    (0, "common"),
    (15, "uncommon"),
    (40, "rare"),
    (100, "epic"),
    (200, "legendary"),
    (500, "mythic")
]
    FLUFF_CUTE_SELL_MULTIPLIER = 1.15
    
    def __init__(self, name, fur_color, eye_color, pattern, size, mood, breed, cuteness, fluffyness, gender):
        self.name = name
        self.fur_color = fur_color
        self.eye_color = eye_color
        self.pattern = pattern
        self.size = size
        self.mood = mood
        self.breed = breed
        self.cuteness = cuteness
        self.fluffyness = fluffyness
        self.gender = gender
        self.cat_rarity = self.calc_cat_rarity()
        self.sell_price = self.calc_cat_sell_price()
        self.xp_value = self.calc_cat_xp()

    def calc_cat_rarity(self):
        data =  self.ATTRIBUTES_DATA       
        attributes_to_check = ["fur_color", "eye_color", "pattern", "size", "mood", "breed"]
        total_points = 0
        for attr in attributes_to_check:
            attr_value = getattr(self, attr)
            rarity = data[attr][attr_value]["rarity"]
            total_points += self.RARITY_POINTS[rarity]
        
        cat_rarity = "common"
        for threshold, rarity_name in self.RARITY_THRESHOLDS:
            if total_points >= threshold:
                cat_rarity = rarity_name
        
        return cat_rarity
        
    def calc_cat_xp(self):
        base_xp = self.RARITY_POINTS[self.cat_rarity] * 10
        bonus = (self.cuteness + self.fluffyness) * self.RARITY_POINTS[self.cat_rarity] // 100
        return int(round((base_xp + bonus), 0))


    def calc_cat_sell_price(self):
        cat_sell_price = self.RARITY_POINTS[self.cat_rarity] + (self.cuteness + self.fluffyness) * self.FLUFF_CUTE_SELL_MULTIPLIER 
        return int(round(cat_sell_price, 0))

    def __str__(self):
        return f"""
        🐱 {self.name} 🐱
        ━━━━━━━━━━━━━━━━━━━━
        🎨 Fur:      {self.fur_color}
        👁️  Eyes:     {self.eye_color}
        🔳 Pattern:  {self.pattern}
        📏 Size:     {self.size}
        😺 Mood:     {self.mood}
        🏷️  Breed:    {self.breed}
        💕 Cuteness: {self.cuteness}/100
        ☁️  Fluffy:   {self.fluffyness}/100
        ⚧️  Gender:   {self.gender}
        ⭐ Rarity:   {self.cat_rarity}
        💰 Sell:     {self.sell_price}
        ✨ XP:       {self.xp_value}
        ━━━━━━━━━━━━━━━━━━━━
        """

    def to_dict(self):
        """Convert Cat to a dictionary for JSON saving."""
        return {
            "name": self.name,
            "fur_color": self.fur_color,
            "eye_color": self.eye_color,
            "pattern": self.pattern,
            "size": self.size,
            "mood": self.mood,
            "breed": self.breed,
            "cuteness": self.cuteness,
            "fluffyness": self.fluffyness,
            "gender": self.gender,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Cat from a dictionary (loaded from JSON) with validation."""
        # Validate required fields exist
        required_fields = ["name", "fur_color", "eye_color", "pattern", "size", "mood", "breed", "cuteness", "fluffyness", "gender"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Cat data is missing required fields: {', '.join(missing_fields)}")

        # Validate data types and ranges
        if not isinstance(data["name"], str) or not data["name"]:
            raise ValueError("Cat name must be a non-empty string")
        if not isinstance(data["cuteness"], (int, float)) or not (0 <= data["cuteness"] <= 100):
            raise ValueError("Cuteness must be between 0 and 100")
        if not isinstance(data["fluffyness"], (int, float)) or not (0 <= data["fluffyness"] <= 100):
            raise ValueError("Fluffyness must be between 0 and 100")
        if data["gender"] not in ["male", "female"]:
            raise ValueError("Gender must be 'male' or 'female'")

        return cls(
            name=data["name"],
            fur_color=data["fur_color"],
            eye_color=data["eye_color"],
            pattern=data["pattern"],
            size=data["size"],
            mood=data["mood"],
            breed=data["breed"],
            cuteness=data["cuteness"],
            fluffyness=data["fluffyness"],
            gender=data["gender"],
        )
    @classmethod   
    def get_catname(cls):
        # Gets catname and removes from catnames.txt
        with open("cat_names.txt", "r") as file:
            names = [line.strip() for line in file if line.strip()] 
        name = random.choice(names)   
        names.remove(name) 
        with open("cat_names.txt", "w") as file:
            file.write("\n".join(names))
        return name
        
    @classmethod
    def get_attribute(cls, attribute: str, box_type: str = "basic"):
        data = cls.ATTRIBUTES_DATA
        attribute_dict = data[attribute]
        
        weights = Box.get_weights(box_type, attribute)
        
        items = []
        item_weights = []
        
        for item_name, item_data in attribute_dict.items():
            items.append(item_name)
            item_weights.append(weights[item_data["rarity"]])
        
        chosen = random.choices(items, weights=item_weights)[0]
        return chosen


    @classmethod
    def unbox_cat(cls, box_type="basic"):
        box = Box.get_box(box_type)
        if not box:
            raise ValueError(f"Unknown box type: {box_type}")
        
        name = cls.get_catname()
        fur_color = cls.get_attribute("fur_color", box_type)
        eye_color = cls.get_attribute("eye_color", box_type)
        pattern = cls.get_attribute("pattern", box_type)
        size = cls.get_attribute("size", box_type)
        mood = cls.get_attribute("mood", box_type)
        breed = cls.get_attribute("breed", box_type)
        cuteness = random.randint(box["min_cute"], box["max_cute"])
        fluffyness = random.randint(box["min_fluffy"], box["max_fluffy"])
        gender = random.choice(["male", "female"])
        
        return cls(name, fur_color, eye_color, pattern, size, mood, breed, cuteness, fluffyness, gender)

    @classmethod
    def can_breed_check(cls, parent1, parent2):
        if parent1.gender == parent2.gender:
            return False, "Parents are same gender"
        else:
            return True, "Can breed"  # Return tuple here too

    @classmethod
    def calc_kitten_cute(cls, parent1, parent2):
        low = min(parent1.cuteness, parent2.cuteness) - 10
        high = max(parent1.cuteness, parent2.cuteness) + 10
        value = random.randint(low, high)
        
        if value > 100:
            return 100
        elif value < 0:
            return 0
        else:
            return value
    
    @classmethod
    def calc_kitten_fluffy(cls, parent1, parent2):
        low = min(parent1.fluffyness, parent2.fluffyness) - 10
        high = max(parent1.fluffyness, parent2.fluffyness) + 10
        value = random.randint(low, high)
        if value > 100:
            return 100
        elif value < 0:
            return 0
        else:
            return value

    @classmethod
    def breed_cats(cls, parent1, parent2):
        can_breed, reason = cls.can_breed_check(parent1, parent2)
        if not can_breed:
            raise ValueError(f"Can't breed: {reason}")
        else:
            name = cls.get_catname()
            fur_color = random.choice([parent1.fur_color, parent2.fur_color])
            eye_color = random.choice([parent1.eye_color, parent2.eye_color])
            pattern = random.choice([parent1.pattern, parent2.pattern])
            size = random.choice([parent1.size, parent2.size])
            mood = random.choice([parent1.mood, parent2.mood])
            breed = random.choice([parent1.breed, parent2.breed])
            cuteness = cls.calc_kitten_cute(parent1, parent2)
            fluffyness = cls.calc_kitten_fluffy(parent1, parent2)
            gender = random.choice(["male", "female"])
            return cls(name, fur_color, eye_color, pattern, size, mood, breed, cuteness, fluffyness, gender)

class Player:
    """Formula: level^power * 100

        Level    power=2    power=1.5    power=1.3
        1          100         100         100
        2          400         283         246
        3          900         520         437
        5        2,500       1,118         891
        10       10,000       3,162       1,995
        20       40,000       8,944       4,481
        50      250,000      35,355      14,563"""
    SAVE_PATH = "save_data.json"
    LEVEL_SCALE_POWER = 1.3

    def __init__(self, name, xp = 0, cat_inventory=None, coins = 0):
        self.name = name
        self.xp = xp
        self.level = self.calc_level()
        self.cat_inventory = cat_inventory if cat_inventory else {}
        self.coins = coins

    def __str__(self):
        inventory_list = "\n".join([f"    - {cat.name} ({cat.cat_rarity})" for cat in self.cat_inventory.values()])
        if not inventory_list:
            inventory_list = "    (empty)"
        
        return f"""
        👤 {self.name}
        ━━━━━━━━━━━━━━━━━━━━
        ⭐ Level:    {self.level}
        ✨ XP:       {self.xp}
        💰 Coins:    {self.coins}
        🐱 Cats:     {len(self.cat_inventory)}
        ━━━━━━━━━━━━━━━━━━━━
        📦 Inventory:
    {inventory_list}
        ━━━━━━━━━━━━━━━━━━━━
        """

    def calc_level(self):
        if self.xp < 100:
            return 1
        level = int((self.xp / 100) ** (1 / self.LEVEL_SCALE_POWER))
        return max(level, 1)
    
    def add_cat(self, cat):
        #  Add a cat to the player's inventory and award XP and calc level 
        # Stores cat in dict by cats name example: inventory["Pearltuft"] is cat object
        self.cat_inventory[cat.name] = cat
        self.xp += cat.xp_value
        self.level = self.calc_level()

    def remove_cat(self, cat_name):
        # Remove a cat from the player's inventory by name. 
        if cat_name in self.cat_inventory:
            return self.cat_inventory.pop(cat_name)
        return None
    
    def sell_cat(self, cat_name):
        cat = self.remove_cat(cat_name)
        if cat:
            self.coins += cat.sell_price
            return cat.sell_price
        return None

    def save_game(self):
        """Save player data to a JSON file."""
        cats_as_dicts = {}
        for name, cat in self.cat_inventory.items():
            cats_as_dicts[name] = cat.to_dict()
        
        data = {
            "name": self.name,
            "xp": self.xp,
            "coins": self.coins,
            "cat_inventory": cats_as_dicts
        }
        
        with open(self.SAVE_PATH, "w") as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_game(cls, filepath):
        """Load player data from a JSON file with validation."""
        try:
            with open(cls.SAVE_PATH, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Save file not found at {cls.SAVE_PATH}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Save file is corrupted or invalid JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading save file: {e}")

        # Validate required fields exist
        required_fields = ["name", "xp", "coins", "cat_inventory"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Save file is missing required fields: {', '.join(missing_fields)}")

        # Validate data types
        if not isinstance(data["name"], str):
            raise ValueError("Player name must be a string")
        if not isinstance(data["xp"], (int, float)) or data["xp"] < 0:
            raise ValueError("XP must be a non-negative number")
        if not isinstance(data["coins"], (int, float)) or data["coins"] < 0:
            raise ValueError("Coins must be a non-negative number")
        if not isinstance(data["cat_inventory"], dict):
            raise ValueError("Cat inventory must be a dictionary")

        # Rebuild cats from dicts with error handling
        cat_inventory = {}
        for name, cat_data in data["cat_inventory"].items():
            try:
                cat_inventory[name] = Cat.from_dict(cat_data)
            except Exception as e:
                print(f"Warning: Failed to load cat '{name}': {e}. Skipping...")
                continue

        return cls(
            name=data["name"],
            xp=int(data["xp"]),
            cat_inventory=cat_inventory,
            coins=int(data["coins"])
        )


