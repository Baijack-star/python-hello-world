import datetime

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def main():
    print("Hello, World!")
    print(f"Current time: {get_current_time()}")

if __name__ == "__main__":
    main()
