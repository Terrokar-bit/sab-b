import math
import time

def calculate_angle(x1, y1, x2, y2):
    """
    Calculates the angle (in radians) from (x1, y1) to (x2, y2).
    WoW Coordinate System:
    X is North(+)/South(-)
    Y is West(+)/East(-)  <-- Check this, usually Y is East/West
    Rotation: 0 is North.
    """
    dx = x2 - x1
    dy = y2 - y1
    
    # atan2(dy, dx) gives angle from X-axis.
    # In WoW, 0 is usually North (Positive X).
    # We might need to adjust this based on testing.
    # Standard atan2 returns -PI to PI.
    angle = math.atan2(dy, dx)
    
    # Normalize to 0 to 2*PI
    if angle < 0:
        angle += 2 * math.pi
        
    return angle

def get_turn_direction(current_yaw, target_yaw):
    """
    Determines best turn direction.
    Returns: 'left', 'right', or None (if facing).
    """
    # Normalize both to 0 - 2PI
    current_yaw = current_yaw % (2 * math.pi)
    target_yaw = target_yaw % (2 * math.pi)
    
    diff = target_yaw - current_yaw
    
    # Normalize diff to -PI to PI
    if diff > math.pi:
        diff -= 2 * math.pi
    if diff < -math.pi:
        diff += 2 * math.pi
        
    # Increased threshold to prevent "jittery" turning
    # 0.5 radians is ~28 degrees. If target is within this cone, we consider it "facing".
    threshold = 0.5 
    
    if abs(diff) < threshold:
        return None
    elif diff > 0:
        return 'left' # WoW rotation increases counter-clockwise? Need to verify.
                      # Usually: Left turn increases angle, Right turn decreases.
    else:
        return 'right'

def turn_towards_target(input_handler, current_yaw, target_yaw):
    direction = get_turn_direction(current_yaw, target_yaw)
    
    if direction == 'left':
        input_handler.press_key('a') # Tap key to turn slightly
    elif direction == 'right':
        input_handler.press_key('d')
    
    return direction is None # Returns True if facing target
