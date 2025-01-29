import json
import os
import subprocess
import sys

CONFIG_FILE = 'config.json'

def load_config(config_path):
    """
    Load the configuration from a JSON file.
    
    :param config_path: Path to the config file.
    :return: Dictionary with configuration data.
    """
    if not os.path.exists(config_path):
        print(f"Configuration file '{config_path}' not found.")
        sys.exit(1)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"Error parsing the configuration file: {e}")
        sys.exit(1)

def display_menu(menu_items):
    """
    Display the menu to the user.
    
    :param menu_items: List of menu items.
    """
    print("\n===== Main Menu =====")
    for idx, item in enumerate(menu_items, start=1):
        print(f"{idx}. {item['title']}")
    print(f"{len(menu_items)+1}. Exit")

def get_user_choice(num_options):
    """
    Get a valid menu choice from the user.
    
    :param num_options: Number of available options.
    :return: The chosen option as an integer.
    """
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= num_options + 1:
                return choice
            else:
                print(f"Please enter a number between 1 and {num_options + 1}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def execute_script(script_path):
    """
    Execute a Python script located at the given path.
    
    :param script_path: Relative path to the Python script.
    """
    if not os.path.exists(script_path):
        print(f"Script '{script_path}' not found.")
        return
    
    # Determine the Python executable
    python_executable = sys.executable
    
    try:
        # Run the script in a new subprocess
        result = subprocess.run([python_executable, script_path], check=True)
        print(f"Script '{script_path}' executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing '{script_path}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    # Load configuration
    config = load_config(CONFIG_FILE)
    
    menu_items = config.get('menu', [])
    
    if not menu_items:
        print("No menu items found in the configuration.")
        sys.exit(1)
    
    while True:
        # Display the menu
        display_menu(menu_items)
        
        # Get user choice
        choice = get_user_choice(len(menu_items))
        
        if choice == len(menu_items) + 1:
            print("Exiting the program. Goodbye!")
            break
        else:
            selected_item = menu_items[choice - 1]
            script_path = selected_item.get('path')
            if script_path:
                execute_script(script_path)
            else:
                print("Invalid configuration: 'path' not found for the selected menu item.")

if __name__ == "__main__":
    main()
