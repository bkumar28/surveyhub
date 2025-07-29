import unittest

import core.api_message as api_message


class TestApiMessage(unittest.TestCase):
    def test_constants(self):
        self.assertIsInstance(api_message.REQUEST_QUERY_PARAM, str)
        self.assertIsInstance(api_message.BAD_REQUEST_ERROR, str)
        self.assertIn("required", api_message.REQUIRED_FIELD.lower())
        self.assertIn("success", api_message.SURVEY_CREATE_SUCCESS.lower())
        self.assertIn(
            "could not be found", api_message.RESOURCE_NOT_FOUND_ERROR.lower()
        )
