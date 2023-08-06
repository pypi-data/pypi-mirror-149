import logging
import requests


class HypClient:
    def __init__(self, access_token, session=requests.Session()):
        self.access_token = access_token
        self.session = session
        self.logger = logging.getLogger("hyp_python_client")

    def assignment(self, participant_id, experiment_id):
        response = self.session.post(
            f'https://app.onhyp.com/api/v1/assign/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token, 'Content-Type': 'application/json'},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result

    def conversion(self, participant_id, experiment_id):
        response = self.session.patch(
            f'https://app.onhyp.com/api/v1/convert/{participant_id}/{experiment_id}',
            headers={'X_HYP_TOKEN': self.access_token, 'Content-Type': 'application/json'},
        )

        result = response.json()
        result["status_code"] = response.status_code

        return result

    def try_api_call(self, method_name, participant_id, experiment_id, fallback):
        if participant_id is None or experiment_id is None:
            missing_data = []
            if participant_id is None:
                missing_data.append("participant ID")

            if experiment_id is None:
                missing_data.append("experiment ID")

            missing_data_message = " and ".join(missing_data)
            self.logger.warning(f'{method_name} failed due to missing {missing_data_message}. Returning fallback {fallback}.')
            return fallback

        response = getattr(self, method_name)(participant_id, experiment_id)

        if response["message"] == "success":
            self.logger.info(f'{method_name} successful for participant {participant_id} in experiment {experiment_id}.')
            if method_name == "assignment":
                return response["payload"]["variant_name"]
            elif method_name == "conversion":
                return response["payload"]["converted"]
        else:
            self.logger.warning(f'{method_name} failed for participant {participant_id} in experiment {experiment_id}. Error: {response["message"]} Returning fallback {fallback}.')
            return fallback

    def try_assignment(self, participant_id, experiment_id, fallback):
        return self.try_api_call("assignment", participant_id, experiment_id, fallback)

    def try_conversion(self, participant_id, experiment_id):
        return self.try_api_call("conversion", participant_id, experiment_id, fallback=False)
