from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces


def main():

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try:
        global speech_config

        # Get config settings
        load_dotenv()
        project_connection = os.getenv('PROJECT_CONNECTION')
        location = os.getenv('LOCATION')

        # Get AI Services key from the project


        # Configure speech service
        

        # Get spoken input
        command = TranscribeCommand()
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition


    # Process speech input


    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
    

    # Synthesize spoken output


    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()