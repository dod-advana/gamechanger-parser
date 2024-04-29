import os
import shutil
import glob

# Function to check if the user has tested the wheel file
def check_tested():
    response = input("Have you tested the wheel file? (y/n): ").strip().lower()
    if response == 'n':
        print("Please test the wheel file before proceeding.")
        return False
    elif response == 'y':
        return True
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        return check_tested()

# Function to find the wheel file and prepare the folder structure
def prepare_wheel_file():
    wheel_files = glob.glob('whl_creation_output/dist/*.whl')
    if not wheel_files:
        raise FileNotFoundError("No wheel file found in whl_creation_output/dist.")

    wheel_path = wheel_files[0]  # Assuming only one wheel file is present
    base_name = os.path.basename(wheel_path).replace("-py3-none-any.whl", "")
    
    # Create the new folder in the current working directory
    new_folder = os.path.join(os.getcwd(), base_name)
    os.makedirs(new_folder, exist_ok=True)

    # Rename and move the wheel file
    new_wheel_path = os.path.join(new_folder, base_name + ".whl")
    shutil.copy(wheel_path, new_wheel_path)

    # Zip build and .egg-info folders
    egg_folder = os.path.basename(wheel_path).replace('-1.0.0-py3-none-any.whl', '')
    for folder_name in ['build', f'{egg_folder}.egg-info']:
        folder_path = os.path.join('whl_creation_output', folder_name)
        if os.path.exists(folder_path):
            shutil.make_archive(os.path.join(new_folder, folder_name), 'zip', folder_path)
        else:
            print(f"Warning: {folder_name} folder does not exist in whl_creation_output.")

    print(f"Preparation complete. Files are in {new_folder}")

# Main function to run the script
def main():
    if check_tested():
        try:
            prepare_wheel_file()
            print("Wheel file has been prepared and stored locally in the current directory.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


# TODO: Ask if you want to upload to s3 : y/n