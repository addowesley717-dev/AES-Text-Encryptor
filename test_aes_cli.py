import unittest
from aes_cli import encrypt_text, decrypt_text


class AesTests(unittest.TestCase):
    def test_round_trip(self):
        msg = "Hello UPSA, Akwaaba! 123"
        self.assertEqual(decrypt_text(encrypt_text(msg, "secret"), "secret"), msg)

    def test_wrong_password_fails(self):
        with self.assertRaises(ValueError):
            decrypt_text(encrypt_text("hi", "right"), "wrong")

    def test_same_text_gives_different_output(self):
        self.assertNotEqual(encrypt_text("hi", "pw"), encrypt_text("hi", "pw"))

    def test_garbage_input(self):
        with self.assertRaises(ValueError):
            decrypt_text("not base64!!", "pw")


if __name__ == "__main__":
    unittest.main()
