"""
Cognitive Loop: The Autonomous Heartbeat of Epsilon Prime.
"""
import time
import sys
import os
import logging
import traceback

# --- PROJECT ROOT ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from tools.autonomy.goal_queue import GoalQueue
from hive.swarm_graph import run_swarm

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [COGNITIVE_LOOP] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(PROJECT_ROOT, "logs", "cognitive_loop.log")),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("CognitiveLoop")

def main():
    logger.info("--- 🔱 COGNITIVE LOOP INITIALIZED ---")
    queue = GoalQueue()
    
    while True:
        try:
            goal = queue.get_next_goal()
            
            if goal:
                goal_id = goal['id']
                goal_text = goal['goal']
                source = goal['source']
                
                logger.info(f"Picked up Goal #{goal_id} from {source}: {goal_text}")
                
                # Update status to processing
                queue.update_status(goal_id, "processing")
                
                # EXECUTE SWARM
                logger.info(f"Engaging Swarm for Goal #{goal_id}...")
                try:
                    result = run_swarm(goal_text)
                    status = "completed"
                    logger.info(f"Goal #{goal_id} SUCCESS. Result: {result[:100]}...")
                except Exception as e:
                    result = f"Swarm Execution Failed: {str(e)}\n{traceback.format_exc()}"
                    status = "failed"
                    logger.error(f"Goal #{goal_id} FAILED: {result}")
                
                # Update final status
                queue.update_status(goal_id, status, result)
                
            else:
                # No goals, sleep
                # logger.debug("Queue empty. Sleeping...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Loop terminated by user.")
            break
        except Exception as e:
            logger.critical(f"CRITICAL LOOP FAILURE: {e}")
            time.sleep(10) # Prevent rapid crash loops

if __name__ == "__main__":
    main()
