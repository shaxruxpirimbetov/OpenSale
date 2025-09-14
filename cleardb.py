import os

# os.chdir("RepProjects/Booking")
path = os.listdir()

if "db.sqlite3" in path:
	os.remove("db.sqlite3")

apps = ["user", "products", "stores"]

for app in apps:
	path = os.listdir(app)
	if "migrations" in path:
		os.chdir(f"{app}/migrations/")
		files = os.listdir()
		
		for file in files:
			if "initial" in file:
				os.remove(file)
		print(os.listdir())

	os.chdir("../..")


print(os.listdir())
