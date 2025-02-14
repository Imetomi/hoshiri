import sys
from command_processor import process_command


def main():
    print("Welcome to Hoshiri Terminal Applet! (Type 'exit' to quit)")

    while True:
        user_input = input("Hoshiri> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            sys.exit()

        process_command(user_input)


if __name__ == "__main__":
    main()
