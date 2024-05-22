import unittest
import json

from slack.view_submission import view_submission


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # Arrange
        data = json.loads('''
{
  "type": "view_submission",
  "view": {
    "type": "modal",
    "blocks": [
      {
        "type": "input",
        "block_id": "K73Vi",
        "label": {
          "type": "plain_text",
          "text": "Name"
        }
      }
    ],
    "state": {
      "values": {
        "K73Vi": {
          "plain_text_input-action": {
            "type": "plain_text_input",
            "value": "Lewis"
          }
        }
      }
    }
  }
}
        ''')

        # Act
        value_by_label = view_submission(data)

        # Assert
        self.assertEqual("Lewis", value_by_label["K73Vi_Name"])


if __name__ == '__main__':
    unittest.main()
