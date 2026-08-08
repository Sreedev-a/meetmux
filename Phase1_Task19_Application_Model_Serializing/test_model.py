import json
import subprocess
import sys
import unittest
from pathlib import Path

from pydantic import ValidationError

from predict import IrisFeatures, load_bundle, predict_one

ROOT = Path(__file__).resolve().parent


class SerializationTests(unittest.TestCase):
    def test_valid_prediction(self):
        result = predict_one(IrisFeatures(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2))
        self.assertEqual(result["class_name"], "setosa")
        self.assertEqual(result["model_version"], "1.0.0")

    def test_validation(self):
        with self.assertRaises(ValidationError):
            IrisFeatures(sepal_length=-1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)

    def test_metadata_and_checksum(self):
        _, metadata = load_bundle()
        self.assertIn("artifact_sha256", metadata)
        self.assertIn("metrics", metadata)

    def test_fresh_process_load(self):
        code = "from predict import *; import json; print(json.dumps(predict_one(IrisFeatures(sepal_length=6.2,sepal_width=2.9,petal_length=4.3,petal_width=1.3))))"
        completed = subprocess.run([sys.executable, "-c", code], cwd=ROOT, text=True, capture_output=True, check=True)
        self.assertIn("model_version", json.loads(completed.stdout))


if __name__ == "__main__":
    unittest.main()
