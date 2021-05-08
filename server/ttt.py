from keystroke_handler import KeystrokeHandler

a = KeystrokeHandler("logged_key.txt")
a.Hook()
m = input("enter...")
a.Unhook()