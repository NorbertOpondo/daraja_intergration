from enum import Enum

class PaymentStatus(Enum):
    ''' enum class for payment statuses'''

    pending = "PENDING"
    complete = "COMPLETE"
    failed = "failed"