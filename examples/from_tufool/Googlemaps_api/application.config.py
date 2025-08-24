import configparser

config = configparser.ConfigParser()
config.read("application.config")

print("HOME address:", config.get("Locations", "HOME"))
print("WORK address:", config.get("Locations", "WORK"))
config = configparser.ConfigParser()
config.read("application.config")

