import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "CLOSED"        # Working fine
    OPEN = "OPEN"            # Failing, reject requests
    HALF_OPEN = "HALF_OPEN"  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=10):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def get_state(self):
        return self.state

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        print(f"✅ Success! State: {self.state.value}")

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        print(f"❌ Failure #{self.failure_count}. State: {self.state.value}")
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(f"⚠️ CIRCUIT BREAKER OPENED!")

    def can_execute(self):
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                print(f"🔄 HALF_OPEN: Testing if service recovered...")
                return True
            return False
        
        if self.state == CircuitState.HALF_OPEN:
            return True
        
        return False