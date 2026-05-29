import json
import unittest

from licensing.internal import HelperMethods
from licensing.methods import AI


class AIUsageAnalyticsTests(unittest.TestCase):

    def _assert_usage_analytics_call(self, call, expected_endpoint, expected_field, expected_params):
        original_send_request = HelperMethods.send_request
        captured = {}

        def fake_send_request(endpoint, params):
            captured["endpoint"] = endpoint
            captured["params"] = params
            return json.dumps({
                "result": 0,
                "message": None,
                expected_field: [{"id": 1}]
            })

        try:
            HelperMethods.send_request = fake_send_request
            result = call()
        finally:
            HelperMethods.send_request = original_send_request

        self.assertEqual(result, ([{"id": 1}], ""))
        self.assertEqual(captured["endpoint"], expected_endpoint)

        for key, value in expected_params.items():
            self.assertEqual(captured["params"][key], value)

    def test_get_daily_aggregates(self):
        self._assert_usage_analytics_call(
            lambda: AI.get_daily_aggregates(
                token="token",
                product_id=123,
                limit=25,
                starting_after=10,
                ending_before=20,
                start="2026-05-01",
                end="2026-05-31"
            ),
            "ai/GetDailyAggregates",
            "aggregates",
            {
                "token": "token",
                "ProductId": 123,
                "Limit": 25,
                "StartingAfter": 10,
                "EndingBefore": 20,
                "Start": "2026-05-01",
                "End": "2026-05-31"
            })

    def test_get_daily_country_aggregates(self):
        self._assert_usage_analytics_call(
            lambda: AI.get_daily_country_aggregates(
                token="token",
                product_id=123,
                country_code="SE"
            ),
            "ai/GetDailyCountryAggregates",
            "aggregates",
            {
                "token": "token",
                "ProductId": 123,
                "CountryCode": "SE"
            })

    def test_get_key_usage_summaries(self):
        self._assert_usage_analytics_call(
            lambda: AI.get_key_usage_summaries(
                token="token",
                product_id=123,
                key_id=456,
                key="AAAA-BBBB-CCCC-DDDD"
            ),
            "ai/GetKeyUsageSummaries",
            "summaries",
            {
                "token": "token",
                "ProductId": 123,
                "KeyId": 456,
                "Key": "AAAA-BBBB-CCCC-DDDD"
            })

    def test_get_key_devices(self):
        self._assert_usage_analytics_call(
            lambda: AI.get_key_devices(
                token="token",
                product_id=123,
                key_id=456,
                machine_code="MACHINE-1"
            ),
            "ai/GetKeyDevices",
            "devices",
            {
                "token": "token",
                "ProductId": 123,
                "KeyId": 456,
                "MachineCode": "MACHINE-1"
            })

    def test_get_license_activity_buckets(self):
        self._assert_usage_analytics_call(
            lambda: AI.get_license_activity_buckets(
                token="token",
                product_id=123,
                key_id=456,
                key="AAAA-BBBB-CCCC-DDDD",
                machine_code="MACHINE-1"
            ),
            "ai/GetLicenseActivityBuckets",
            "buckets",
            {
                "token": "token",
                "ProductId": 123,
                "KeyId": 456,
                "Key": "AAAA-BBBB-CCCC-DDDD",
                "MachineCode": "MACHINE-1"
            })


if __name__ == "__main__":
    unittest.main()
