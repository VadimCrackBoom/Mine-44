class CommandHandler:
    @staticmethod
    def execute(command, terminal):
        terminal.add_to_output(f"> {command}")

        if command == "help":
            return CommandHandler.help(terminal)
        elif command == "clear":
            return CommandHandler.clear(terminal)
        elif command == "setup/confidence.bat":
            return CommandHandler.setup(terminal)
        elif command == "scan":
            return CommandHandler.scan(terminal)
        elif command == "decrypt":
            return CommandHandler.decrypt(terminal)
        elif command == "exit":
            return False  # сигнал для выхода
        else:
            terminal.add_to_output(f"Command not recognized: {command}")
            return True

    @staticmethod
    def help(terminal):
        terminal.add_to_output("Available commands:")
        terminal.add_to_output("help - Show this help message")
        terminal.add_to_output("clear - Clear the terminal")
        terminal.add_to_output("setup/confidence.bat - Initialize system protocol")
        terminal.add_to_output("scan - Run network scan")
        terminal.add_to_output("decrypt - Start decryption sequence")
        terminal.add_to_output("page <num> - Switch to page <num>")
        terminal.add_to_output("exit - Close the terminal")
        return True

    @staticmethod
    def clear(terminal):
        terminal.clear_output()
        return True

    @staticmethod
    def setup(terminal):
        terminal.add_to_output("Initializing system protocol...")
        terminal.add_to_output("Loading core modules...")
        terminal.start_progress()
        return True

    @staticmethod
    def scan(terminal):
        terminal.add_to_output("Scanning network...")
        terminal.add_to_output("Discovering devices...")
        for i in range(1, 8):
            status = "Protected" if i % 3 == 0 else "Vulnerable"
            terminal.add_to_output(f"Device 192.168.1.{i} - Status: {status} - OS: {'Windows' if i % 2 else 'Linux'}")
        terminal.add_to_output("Scan complete. 7 devices found.")
        return True

    @staticmethod
    def decrypt(terminal):
        terminal.add_to_output("Starting decryption sequence...")
        terminal.add_to_output("Initializing quantum decoder...")
        for i in range(1, 6):
            result = "SUCCESS" if i % 2 else "FAILED"
            terminal.add_to_output(f"Layer {i}: {result} - {'Key accepted' if i % 2 else 'Invalid checksum'}")
        terminal.add_to_output("Decryption process completed.")
        return True