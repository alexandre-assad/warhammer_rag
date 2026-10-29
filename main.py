from pathlib import Path

from infra.databases.database import execute_select


def main():
    print("Hello from school-rag-lab-1!")


if __name__ == "__main__":
    print(execute_select('select * from abilities'))