import bluetooth
from PyOBEX.client import Client

addr = 'AC:22:0B:E3:16:84'

devices = {
	'scout1': 'AC:22:0B:E3:1A:26',
	#'scout2': 'AC:22:0B:E3:14:AE',
	#'scout5': 'AC:22:0B:E3:16:84',
	#'blue_super': 'AC:22:0B:5E:A2:41',
}
for device in devices:
	print("Sending to %s..." % device)
	service_matches = bluetooth.find_service(name=b'OBEX Object Push', address = devices[device] )
	print(service_matches)
	if len(service_matches) == 0:
	    print("[W] %s not found, not sent." % device)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print("Connecting to \"%s\" on %s" % (name, host))
	client = Client(host, port)
	client.connect()
	client.put("backupFile.txt", "Hello world\n")
	client.disconnect()
	print("Successfuly sent to %s." % device)
