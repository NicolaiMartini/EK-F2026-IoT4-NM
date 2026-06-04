import datetime
import backend

if __name__ == "__main__":
    try:
        print("Extraction begun")
        backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$",f"/tmp/{datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}/")
    except Exception as e:
        print(e)
