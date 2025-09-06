import json
import random
import os
import traceback

def get_recent_messages():
    """Get recent messages from stored_data.json with proper error handling"""
    
    print("📚 Loading recent messages...")
    
    # Use absolute path to ensure file is found regardless of where the function is called from
    try:
        # Get the directory of the current file (database.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the backend directory
        backend_dir = os.path.dirname(current_dir)
        file_name = os.path.join(backend_dir, "stored_data.json")
        
        print(f"📁 Looking for file: {file_name}")
    except Exception as e:
        print(f"❌ Error constructing file path: {str(e)}")
        # Fallback to simple relative path
        file_name = "stored_data.json"

    # Define the learn instruction
    learn_instruction = {
        "role": "system",
        "content": "You are a sales person selling cars and houses  . Ask relevant Q , user is Noufal. Keep your answer under 25 words with simple language to understand."
    }

    # Initialize messages list with learn instruction
    messages = []

    # Add random element 
    x = random.randint(0, 1)
    if x < 0.5:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some  humour."
    else:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a rather user freandly qustion."  

    # Append instruction to messages
    messages.append(learn_instruction)
    print(f"✅ System instruction added: {learn_instruction['content'][:50]}...")

    # Get last messages
    try:
        # Make sure file exists before trying to open it
        if os.path.exists(file_name):
            print(f"📖 Reading file: {file_name}")
            with open(file_name, 'r', encoding='utf-8') as user_file:
                data = json.load(user_file)

            # Append last 5 items of data 
            if data:
                if len(data) < 5:
                    # If less than 5 messages, append all
                    for item in data:
                        messages.append(item)
                    print(f"📚 Loaded {len(data)} messages (all available)")
                else:
                    # Get the last 5 messages (most recent conversation)
                    for item in data[-5:]:
                        messages.append(item)
                    print(f"📚 Loaded last 5 messages from {len(data)} total")
            else:
                print("📚 No conversation history found")
        else:
            print(f"📁 File not found: {file_name}, using only system instructions")
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {str(e)}")
        print("🔧 The stored_data.json file may be corrupted")
    except Exception as e:
        print(f"❌ Error reading messages: {str(e)}")
        print(traceback.format_exc())

    print(f"✅ Returning {len(messages)} messages total")
    return messages

def store_messages(request_message, response_message):
    """Store messages to stored_data.json with proper error handling"""
    
    print(f"💾 Storing messages: User='{request_message[:30]}...', Assistant='{response_message[:30]}...'")
    
    # Define the file name (use simple relative path for storage)
    file_name = "stored_data.json"

    try:
        # Load existing messages (excluding system instruction)
        existing_data = []
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                print(f"📖 Loaded {len(existing_data)} existing messages")
            except json.JSONDecodeError:
                print("🔧 Corrupted JSON file, starting fresh")
                existing_data = []

        # Add new messages to data
        user_message = {"role": "user", "content": request_message}
        assistant_message = {"role": "assistant", "content": response_message}
        
        existing_data.append(user_message)
        existing_data.append(assistant_message)

        # Save the updated file
        with open(file_name, "w", encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Messages stored successfully. Total messages: {len(existing_data)}")
        
    except Exception as e:
        print(f"❌ Error storing messages: {str(e)}")
        print(traceback.format_exc())
        raise e

def reset_messages():
    """Reset messages by clearing stored_data.json"""
    
    print("🔄 Resetting conversation history...")
    
    file_name = "stored_data.json"
    
    try:
        # Overwrite the stored_data.json file with an empty list
        with open(file_name, "w", encoding='utf-8') as f:
            json.dump([], f)
        
        print("✅ Conversation history reset successfully")
        
    except Exception as e:
        print(f"❌ Error resetting messages: {str(e)}")
        print(traceback.format_exc())
        raise e