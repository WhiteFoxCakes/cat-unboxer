import random
import time
import json
import attr

class Cat:
    def __init__(self, name, fur_color, eye_color, pattern, size, mood, breed, cuteness = 0, fluffyness = 0):
        self.name = name
        self.fur_color = fur_color
        self.eye_color = eye_color
        self.pattern = pattern
        self.size = size
        self.mood = mood
        self.breed = breed
        self.cuteness = cuteness
        self.fluffyness = fluffyness

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
            chosen_attribute = random.choice(list(attribute_dict.keys()))
            return chosen_attribute
   
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
        return cls(name, fur_color, eye_color, pattern, size, mood, breed, cuteness, fluffyness)



my_cat = Cat.unbox_cat()
print(my_cat)