import unittest
import socket

class TestServer(unittest.TestCase):
	
	test_cases = [
			[
	       		"request too short",
	       		bytes([0, 1, 1, 1]),
	       		bytes([5])
	 		],
	    	[
	    		"unsupported protocol",	
	    		bytes([0, 0, 1, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
	    		bytes([1])
	       ],
	       [
	       		"invalid cmd",
	       		bytes([0, 1, 10, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
	       		bytes([2])
	       ],
	       [
	       		"invalid userid",
	       		bytes([0, 1, 1, 1, 32, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
	       		bytes([103])
	       ],
	       [
	       		"register bahojsiboflobutsujar",
	       		bytes([0, 1, 1, 1, 98, 97, 104, 111, 106, 115, 105, 98, 111, 102, 108, 111, 98, 117, 116, 115, 117, 106, 97, 114]),
	       		bytes([201, 115, 116, 117, 97, 114, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	       ]
	    ]

	def setUp(self):
		self.client = socket.socket()
		self.client.settimeout(1)
		self.client.connect(('127.0.0.1', 8080))

	def tearDown(self):
		self.client.close()

	def get_response_for_request(self, request):
		self.client.send(request)
		response = self.client.recv(1024)
		return response

	def testIt(self):
		for name,request,expected_response in self.test_cases:
			response = self.get_response_for_request(request)
			self.assertEqual(response, expected_response, "test " + name + " failed. response: " + str(list(response)) + " not: " + str(list(expected_response)))

if __name__ == '__main__':
    unittest.main()		
