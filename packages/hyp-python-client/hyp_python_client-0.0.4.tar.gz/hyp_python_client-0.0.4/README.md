# hyp_python_client
Python API client for [Hyp](https://onhyp.com/).

# Installation
```shell
pip install hyp-python-client
```

# Usage
The most basic usage of the client is to call the Hyp API endpoints for assignment
of a participant into an experiment variant and for conversion of a participant
in a particular experiment:
```python
from hyp_client.v1 import HypClient

# This is a real access token for a dummy data account on Hyp. Feel free to use
# it to test out the API.
client = HypClient(access_token="PRODUCTION/HYP/5ab8d3d8-6eca-4e11-9203-1b64faea1f33")
client.assignment(participant_id="fuzzybear", experiment_id=8)
# {'payload': {'variant_id': 18, 'variant_name': 'v2'}, 'message': 'success', 'status_code': 200}

client.conversion(participant_id="fuzzybear", experiment_id=8)
# {'payload': {'converted': True}, 'message': 'success', 'status_code': 200}

# No experiment found
client.assignment(participant_id="fuzzybear", experiment_id=13)
# {'payload': '', 'message': 'No experiment with ID 13 was found.', 'status_code': 404}

client.conversion(participant_id="fuzzybear", experiment_id=13)
# {'payload': '', 'message': 'No variant assignment for participant fuzzybear in experiment 8 was found. Participants must be assigned to a variant before conversion can be recorded.', 'status_code': 404}
```

The client also provides convenience methods for the common task of calling the
API, parsing the response, and handling errors. For example in your application
you could write code like the following:
```python
from hyp_client.v1 import HypClient

client = HypClient("PRODUCTION/HYP/5ab8d3d8-6eca-4e11-9203-1b64faea1f33")
response = client.assignment(participant_id="fuzzybear", experiment_id=8)
variant = "Red button color"

if response["message"] == "success":
  variant = response["payload"]["variant_name"]
```

To avoid this boilerplate you can use the `try_assignment` and `try_conversion`
methods:
```python
variant = self.client.try_assignment(participant_id="fuzzybear", experiment_id=8, fallback="some variant name")
# API call was successful, `variant` is "v2"

variant = self.client.try_assignment(participant_id="fuzzybear", experiment_id=13, fallback="some variant name")
# API call was unsuccessful because there is no experiment with ID 13.
# `variant` is "some variant name"

converted = self.client.try_conversion(participant_id="fuzzybear", experiment_id=8)
# API call was successful, `converted` is True

converted = self.client.try_conversion(participant_id="fuzzybear", experiment_id=13)
# API call was unsuccessful both because there is no experiment with ID 13 and
# there is no assignment for "fuzzybear" in that experiment.
# `converted` is False.
```

These methods will call the API and return the relevant result if the API call
was successful. In the case of `try_assignment` the result is the name of the
variant. In the case of `try_conversion` the result is the boolean `True`, confirming
that the participant was marked as converted for that experiment.

If the API call returns a non-200 response code for some reason `try_assignment`
will return the provided `fallback` and `try_conversion` will return `False`.

Regardless of whether or not the API call is successful, these methods also log
out info about what has happened. They use a logger named `"hyp_python_client"`
and log out at the `info` level if the API call is successful and at the `warning`
level if the call was unsuccessful. The log messages will pass include any error
message from the server and look like this:
```python
variant = self.client.try_assignment(participant_id="fuzzybear", experiment_id=8, fallback="some variant name")
# => assignment successful for participant fuzzybear in experiment 8.

variant = self.client.try_assignment(participant_id="fuzzybear", experiment_id=13, fallback="some variant name")
# => assignment failed for participant sillybear in experiment 888. Error: No experiment with ID 13 was found. Returning fallback some variant name.

# Missing data:
variant = self.client.try_assignment(participant_id=None, experiment_id=None, fallback="some variant name")
# => assignment failed due to missing participant ID and experiment ID. Returning fallback some variant name.

converted = self.client.try_conversion(participant_id="fuzzybear", experiment_id=8)
# => conversion successful for participant fuzzybear in experiment 8.

converted = self.client.try_conversion(participant_id="fuzzybear", experiment_id=13)
# => conversion failed for participant sillybear in experiment 13. Error: No variant assignment for participant sillybear in experiment 888 was found. Participants must be assigned to a variant before conversion can be recorded. Returning fallback False.

converted = self.client.try_conversion(participant_id="fuzzybear", experiment_id=None)
# => conversion failed due to missing experiment ID. Returning fallback False.
```

# Developing and running the tests
We recommend using a virtual environment to isolate your installed packages.

```python
python -m pip install -r requirements.txt
python -m unittest discover tests
```
