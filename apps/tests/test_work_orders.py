import unittest

from app.db.models.work_order import WorkOrderStatus
from app.modules.work_orders.status_flow import is_transition_allowed, require_valid_transition


class TestWorkOrderStatusFlow(unittest.TestCase):
    def test_transition_matrix(self) -> None:
        self.assertTrue(is_transition_allowed(WorkOrderStatus.open, WorkOrderStatus.in_progress))
        self.assertFalse(is_transition_allowed(WorkOrderStatus.completed, WorkOrderStatus.open))

    def test_require_valid_transition_raises(self) -> None:
        with self.assertRaises(ValueError):
            require_valid_transition(WorkOrderStatus.cancelled, WorkOrderStatus.open)
