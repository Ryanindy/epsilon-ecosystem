import math
import time

def crash_test():
    print("[TEST] Triggering NameError...")
    # 'math' is not imported. This should trigger the Healer.
    return math.sqrt(16)

if __name__ == "__main__":
    crash_test()
