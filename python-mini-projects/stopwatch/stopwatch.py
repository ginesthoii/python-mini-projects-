import time

def main():
    input("Press Enter to start...")
    start = time.time()
    input("Press Enter to stop...")
    elapsed = time.time() - start
    print(f"Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
