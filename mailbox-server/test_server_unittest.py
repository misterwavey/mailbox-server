import unittest
import socket

class TestServer(unittest.TestCase):
	INVALID_REQUEST = bytes([0,1])
	EXPECTED = bytes([5])

	def setUp(self):
		self.client = socket.socket()
		self.client.settimeout(1)
		self.client.connect(('127.0.0.1', 8080))

	def get_response_for_request(self, request):
		self.client.send(request)
		response = self.client.recv(1024)
		self.client.close()
		return response

	def testInvalidLength(self):
		response = self.get_response_for_request(self.INVALID_REQUEST)
		self.assertEqual(response, self.EXPECTED, "not expected")

if __name__ == '__main__':
    unittest.main()		
