import backend

if __name__ == "__main__":
    try:
        print("Extracting:")
        backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$")
    except Exception as e:
        print(e)
