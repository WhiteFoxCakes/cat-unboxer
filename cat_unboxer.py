from classes import Player, Cat, Box, Shop


def main():
    main_menu()


def main_menu():
    while True:
        display_main_menu()
        u_input = input("Select option: ")
        
        if u_input == "1":
            try:
                player = Player.load_game(Player.SAVE_PATH)
                print(f"\nWelcome back, {player.name}!")
            except FileNotFoundError:
                name = input("Enter your name: ")
                player = Player(name, coins=500)
                print(f"\nWelcome, {player.name}! Here's 500 coins to start.")
            
            game_menu(player)
            
        elif u_input == "2":
            print("Goodbye!")
            break
            
        else:
            print("Invalid input")


def game_menu(player):
    while True:
        display_game_menu()
        u_input = input("Select option: ")
        
        if u_input not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Invalid input")
            continue
            
        match u_input:
            case "1":
                shop_menu(player)
            case "2":
                inventory_menu(player)
            case "3":
                sell_menu(player)
            case "4":
                breed_menu(player)
            case "5":
                print(player)
            case "6":
                player.save_game()
                print("✅ Game saved!")
            case "7":
                print("Returning to main menu...")
                break


def shop_menu(player):
    Shop.display_shop()
    print(f"💰 Your coins: {player.coins}")
    box_choice = input("Enter box name (or 'back'): ").lower().strip()
    
    if box_choice == "back":
        return
    
    try:
        cats = Shop.buy_box(player, box_choice)
        print("\n🎉 You got:")
        for cat in cats:
            print(cat)
        print(f"💰 Remaining coins: {player.coins}")
    except ValueError as e:
        print(f"❌ {e}")


def inventory_menu(player):
    if not player.cat_inventory:
        print("\n📦 Your inventory is empty!")
        return
    
    print(f"\n📦 YOUR CATS ({len(player.cat_inventory)}) 📦")
    print("━" * 35)
    
    for i, (name, cat) in enumerate(player.cat_inventory.items(), 1):
        print(f"{i}. {name} - {cat.cat_rarity} ({cat.breed})")
    
    print("━" * 35)
    view_choice = input("Enter cat name to view details (or 'back'): ").strip()
    
    if view_choice.lower() == "back":
        return
    
    if view_choice in player.cat_inventory:
        print(player.cat_inventory[view_choice])
    else:
        print("❌ Cat not found.")


def sell_menu(player):
    if not player.cat_inventory:
        print("\n📦 Your inventory is empty!")
        return
    
    print("\n💰 SELL CATS 💰")
    print("━" * 35)
    
    for name, cat in player.cat_inventory.items():
        print(f"  {name} - {cat.cat_rarity} - 💰{cat.sell_price} coins")
    
    print("━" * 35)
    print(f"Your coins: {player.coins}")
    sell_choice = input("Enter cat name to sell (or 'back'): ").strip()
    
    if sell_choice.lower() == "back":
        return
    
    if sell_choice in player.cat_inventory:
        price = player.sell_cat(sell_choice)
        print(f"✅ Sold {sell_choice} for {price} coins!")
        print(f"💰 New balance: {player.coins}")
    else:
        print("❌ Cat not found.")


def breed_menu(player):
    # Check if enough cats
    if len(player.cat_inventory) < 2:
        print("\n❌ You need at least 2 cats to breed!")
        return
    
    print("\n💕 BREED CATS 💕")
    print("━" * 35)
    
    for name, cat in player.cat_inventory.items():
        print(f"  {name} - {cat.gender} - {cat.breed}")
    
    print("━" * 35)
    
    parent1_name = input("Enter first parent name (or 'back'): ").strip()
    if parent1_name.lower() == "back":
        return
    
    if parent1_name not in player.cat_inventory:
        print("❌ Cat not found.")
        return
    
    parent2_name = input("Enter second parent name: ").strip()
    if parent2_name not in player.cat_inventory:
        print("❌ Cat not found.")
        return
    
    if parent1_name == parent2_name:
        print("❌ Can't breed a cat with itself!")
        return
    
    parent1 = player.cat_inventory[parent1_name]
    parent2 = player.cat_inventory[parent2_name]
    
    try:
        kitten = Cat.breed_cats(parent1, parent2)
        player.add_cat(kitten)
        print("\n🎉 New kitten born!")
        print(kitten)
    except ValueError as e:
        print(f"❌ {e}")


def display_game_menu():
    print("\n🎮 GAME MENU 🎮")
    print("━" * 25)
    print("  1. Shop")
    print("  2. Inventory")
    print("  3. Sell")
    print("  4. Breed")
    print("  5. Stats")
    print("  6. Save")
    print("  7. Quit")
    print("━" * 25)


def display_main_menu():
    print("\n🐱 CAT UNBOXER 🐱")
    print("━" * 25)
    print("  1. Start Game")
    print("  2. Quit")
    print("━" * 25)


if __name__ == "__main__":
    main()