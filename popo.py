import json
from argparse import ArgumentParser

import requests

parser = ArgumentParser()

parser.add_argument(
  "-d", "--district",
  choices=[
    "Oslo",
    "Agder",
    "Finnmark",
    "Innlandet",
    "Møre og Romsdal",
    "Norland",
    "Øst",
    "Sør-Øst",
    "Sør-Vest",
    "Troms",
    "Trøndelag",
    "Vest"
  ]
)

parser.add_argument(
  "-m", "--max",
  default=10,
  type=int
)

parser.add_argument(
  "-a",
  help="Only show active messages",
  dest="activeOnly",
  action="store_true"
)

args = parser.parse_args()

def get_data():
  data = {
    "Take": args.max,
    "Category": [],
  }

  if(args.district):
    data["district"] = f"{args.district} Politidistrikt"

  res = requests.post(
    url="https://politiloggen-vis-frontend.bks-prod.politiet.no/api/messagethread",
    headers={
      'Content-Type': 'application/json'
    },
    data=json.dumps(data)
  )

  if(not res.ok):
    return None
  
  return res.json()

if __name__ == "__main__":
  data = get_data()

  if(data is None):
    print("Failed to get data")
    exit(1)

  messages = data.get("messageThreads")

  for m in messages:
    if(not m.get("isActive") and args.activeOnly):
      continue

    big_place = m.get("municipality")
    area = m.get("area")
    category = m.get("category")
    sub_messages = m.get("messages")

    print(f"[{category}: {big_place}, {area}]: ")
    for sub_m in sub_messages:
      txt = sub_m.get("text")
      
      print("\t", end="")
      if(sub_m.get("hasImage")):
        print("[IMAGE]: ", end="")
      
      print(txt)
    print()


