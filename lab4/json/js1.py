import json

with open("sample-data.json", "r") as file:
    data = json.load(file)


print("Interface status")
print("=" * 80)
print("DN", " " * 40, "Description ", "speed", " " * 10, "MTU")
print("-" * 41, "-" * 12, "-" * 13, "\t", "-" * 4)


for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    print(attributes["dn"], "\t\t", attributes["speed"], "\t", attributes["mtu"])