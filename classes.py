import random
import time
import json



def chance(percent):
    return random.random() < percent / 100

class Cat:
    IMPOTENT_CHANCE = 7
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
    
    def __init__(self, name, fur_color, eye_color, pattern, size, mood, breed, cuteness = 0, fluffyness = 0, gender = "male", impotent = False):
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
        self.impotent = impotent
        self.cat_rarity = self.calc_cat_rarity()
        self.sell_price = self.calc_cat_sell_price()
        self.xp_value = self.calc_cat_xp()

    def calc_cat_rarity(self):
        with open("cat_attributes.json", "r") as file:
            data = json.load(file)
        
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
        return base_xp + bonus


    def calc_cat_sell_price(self):
        cat_sell_price = self.RARITY_POINTS[self.cat_rarity] + (self.cuteness + self.fluffyness) * self.FLUFF_CUTE_SELL_MULTIPLIER 
        return cat_sell_price

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
        ━━━━━━━━━━━━━━━━━━━━
        """
    # Add these to your Cat class

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
            "impotent": self.impotent
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Cat from a dictionary (loaded from JSON)."""
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
            impotent=data["impotent"]
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
    def get_attribute(cls, attribute: str):
        with open("cat_attributes.json", "r") as file:
            data = json.load(file)
        
        attribute_dict = data[attribute]
        
        items = []
        weights = []
        
        for item_name, item_data in attribute_dict.items():
            items.append(item_name)
            weights.append(cls.RARITY_WEIGHTS[item_data["rarity"]])
        
        chosen = random.choices(items, weights=weights)[0]
        return chosen


    @classmethod
    def unbox_cat(cls):
        name = cls.get_catname()
        fur_color = cls.get_attribute("fur_color")
        eye_color = cls.get_attribute("eye_color")
        pattern = cls.get_attribute("pattern")
        size = cls.get_attribute("size")
        mood = cls.get_attribute("mood")
        breed = cls.get_attribute("breed")
        cuteness = random.randint(0, 100)
        fluffyness = random.randint(0, 100)
        gender = random.choice(["male", "female"])
        impotent = chance(cls.IMPOTENT_CHANCE)
        return cls(name, fur_color, eye_color, pattern, size, mood, breed, cuteness, fluffyness, gender, impotent)

    @classmethod
    def can_breed_check(cls, parent1, parent2):
        if parent1.gender == parent2.gender:
            return False, "Parents are same gender"
        elif parent1.impotent or parent2.impotent:
            return False, "One parent is impotent"
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
            impotent = chance(cls.IMPOTENT_CHANCE)
            return cls(name, fur_color, eye_color, pattern, size, mood, breed, cuteness, fluffyness, gender, impotent)

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
    LEVEL_SCALE_POWER = 1.3

    def __init__(self, name, xp = 0, cat_inventory=None, coins = 0):
        self.name = name
        self.xp = xp
        self.level = self.calc_level()
        self.cat_inventory = cat_inventory if cat_inventory else {}
        self.coins = coins

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

my_cat1 = Cat.unbox_cat()
my_cat2 = Cat.unbox_cat()
my_cat3 = Cat.breed_cats(my_cat1, my_cat2)
print(my_cat1, my_cat2, my_cat3)