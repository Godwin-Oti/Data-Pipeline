import openeo

connection = openeo.connect("https://earthengine.openeo.org")
print(connection.list_collections())
print(connection.list_processes())
