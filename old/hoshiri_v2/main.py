# main.py
from hoshiri.engine import HoshiriEngine
from hoshiri.utils.animations import thinking_animation, processing_animation


def main():
    print("Welcome to Hoshiri Terminal!")
    engine = HoshiriEngine()

    while True:
        command = input("\nEnter command (or 'quit' to exit): ")
        if command.strip().lower() == "quit":
            print("Goodbye!")
            break

        thinking_animation()
        response = engine.handle_command(command)
        processing_animation()
        print("\nHoshiri:", response)


if __name__ == "__main__":
    main()
