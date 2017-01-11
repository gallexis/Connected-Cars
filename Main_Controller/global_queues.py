import queue

# Global Queues

CONTROLLER_IN_Q = queue.Queue()

TO_MASTER_Q = queue.Queue()
TO_SLAVE_Q = queue.Queue()
TO_MOTORS_Q = queue.Queue()
