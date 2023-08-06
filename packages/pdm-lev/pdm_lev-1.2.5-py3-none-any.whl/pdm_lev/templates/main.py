import levrt
from {project_name} import hello

async def main():
    doc = await hello()
    data = await doc.get()
    print(data["msg"])


if __name__ == "__main__":
    levrt.run(main())
