import unittest
from pyserver_client.server import Server, ExecuteCommandError
from tempfile import TemporaryFile, TemporaryDirectory
import os
import re

# import sys
# sys.stderr = open("test_error.log", 'a')

class Config:
    SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", None)
    if SERVER_ADDRESS is None:
        raise ValueError("Bad value for server address. "
                         "Example: export SERVER_ADDRESS=192.168.44.44:2014@root:password")
    SERVER_IP, \
    SERVER_PORT, \
    SERVER_USER, \
    SERVER_PASSWORD = re.split(r":|@", SERVER_ADDRESS)
    SERVER_PORT = int(SERVER_PORT)


class TestServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_01_welcome(self):
        target = "/tmp/hello_world.txt"
        with Server(Config.SERVER_IP, Config.SERVER_USER, port=Config.SERVER_PORT,
                    password=Config.SERVER_PASSWORD) as server:
            response = server.shell('echo "Welcome ${USER}!"')
            self.assertEqual([f'Welcome {Config.SERVER_USER}!\n'], response.rows)

            # with TemporaryFile() as temp:
            #     byte_text = b"Create temp file.\n"
            #     temp.write(byte_text)
            #     temp.seek(0)
            #     breakpoint()
            #     server.put_file(temp, target)  # upload file to server
            #     res = server.shell(f'[[ -f {target} ]] && echo "file"')
            #     self.assertEqual(0, res.return_code())
            #     self.assertEqual(['file\n'], res.rows)
            #     with TemporaryDirectory() as tmpdirname:
            #         local_file = os.path.join(tmpdirname, "from_server.txt")
            #         server.get_file(target, local_file)  # download file from server
            #         with open(local_file, "rb") as f:
            #             data = f.read()
            #         self.assertEqual(byte_text, data)
            #
            #     sftp = server.get_sftp()
            #     sftp.remove(target)
            #     res = server.shell(f'[[ -f {target} ]] && echo "file"')
            #     self.assertEqual(1, res.return_code())

    def test_02_struct_shell(self):
        with Server(Config.SERVER_IP, Config.SERVER_USER, port=Config.SERVER_PORT,
                    password=Config.SERVER_PASSWORD) as server:
            server.struct_shell("ls -la")
            with self.assertRaises(ExecuteCommandError):
                server.struct_shell("ldasds -la")


    @classmethod
    def tearDownClass(cls):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestServices('test_login_action'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())