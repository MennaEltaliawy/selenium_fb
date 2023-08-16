import configparser

config = configparser.ConfigParser()
config.read('config.ini')

print(config.sections())

for section in config.sections():
    print(section)
    print(config[section])
    for key, value in config[section].items():
        print(key, value)