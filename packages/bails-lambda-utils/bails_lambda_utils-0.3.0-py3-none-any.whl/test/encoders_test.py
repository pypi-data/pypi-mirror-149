import json
from dataclasses import dataclass
from datetime import datetime
from bails_lambda_utils.encoders import ModelEncoder


@dataclass
class FakeModel:
    attribute_values: object


@dataclass
class FakeModel2:
    attribute_values: object

    def get_legacy_fields(self):
        return {"old": "really old"}


def test_model_encoder_handles_dict():
    model = {"id": 123}
    json_model = json.dumps(model, cls=ModelEncoder)
    assert json_model == '{"id": 123}'


def test_model_encoder_handles_model():
    model = FakeModel(attribute_values={"id": 123})
    json_model = json.dumps(model, cls=ModelEncoder)
    assert json_model == '{"id": 123}'


def test_model_encoder_handles_dates():
    json_model = json.dumps(datetime.now(), cls=ModelEncoder)
    assert json_model is not None


def test_model_encoder_handles_set():
    json_model = json.dumps({3}, cls=ModelEncoder)
    assert json_model == "[3]"
