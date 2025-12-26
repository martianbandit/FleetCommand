import unittest

from app.db.models.repair_request import RepairRequestStatus
from app.modules.repair_requests.schemas import RepairRequestResponse


class TestRepairRequestSchemas(unittest.TestCase):
    def test_response_model_accepts_status(self) -> None:
        response = RepairRequestResponse(
            id="req-1",
            vehicle_id="vehicle-1",
            driver_id="driver-1",
            description="Replace brake pads",
            status=RepairRequestStatus.submitted,
        )

        self.assertEqual(response.status, RepairRequestStatus.submitted)
        self.assertEqual(response.description, "Replace brake pads")
