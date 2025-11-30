import time
from memory import MemoryReader
from input_handler import InputHandler
import offsets
import movement
import math

def find_object_by_guid(memory, client_conn_addr, target_guid):
    """
    Walks the Object Manager to find an object with the specific GUID.
    """
    if not client_conn_addr or not target_guid: return 0
    
    try:
        object_manager_addr = memory.read_int(client_conn_addr + offsets.OFFSET_CLIENT_CONN_CUR_MGR)
        if not object_manager_addr: return 0

        current_object = memory.read_int(object_manager_addr + offsets.OFFSET_OBJ_MGR_FIRST_OBJ)
        
        loop_count = 0
        while current_object and current_object != 0 and (current_object % 2 == 0) and loop_count < 10000:
            loop_count += 1
            try:
                obj_guid = memory.read_ulong(current_object + offsets.OFFSET_OBJ_GUID)
            except:
                break
            
            if obj_guid == target_guid:
                return current_object
            
            current_object = memory.read_int(current_object + offsets.OFFSET_OBJ_MGR_NEXT_OBJ)
    except Exception as e:
        print(f"Error in Object Manager walker: {e}")
    
    return 0

def main():
    print("AntiWowBot initialized.")
    
    # Initialize modules
    memory = MemoryReader("Wow.exe") # Adjust process name if needed
    input_handler = InputHandler()

    # Try to attach to game
    if memory.attach():
        print("Ready to bot! (Press Ctrl+C to stop)")
        try:
            # State tracking
            is_moving = False

            while True:
                # 1. Read Local Player GUID
                local_player_guid = memory.read_ulong(offsets.STATIC_PLAYER_GUID)
                
                # 2. Get Client Connection
                client_conn_addr = memory.read_int(offsets.STATIC_CLIENT_CONNECTION)
                
                if not client_conn_addr:
                    print("Could not read Client Connection pointer.")
                    time.sleep(1)
                    continue

                # 3. Find Local Player Object
                player_obj_addr = find_object_by_guid(memory, client_conn_addr, local_player_guid)

                if player_obj_addr:
                    # Read Descriptor Pointer
                    descriptor_ptr = memory.read_int(player_obj_addr + offsets.OFFSET_DESCRIPTOR_PTR)
                    
                    if descriptor_ptr:
                        # Read Verified Values
                        level = memory.read_int(descriptor_ptr + offsets.OFFSET_UNIT_LEVEL)
                        current_health = memory.read_int(descriptor_ptr + offsets.OFFSET_UNIT_HEALTH)
                        max_health = memory.read_int(descriptor_ptr + offsets.OFFSET_UNIT_MAX_HEALTH)
                        
                        # Read Target GUID
                        target_guid = memory.read_ulong(descriptor_ptr + offsets.OFFSET_UNIT_TARGET)
                        
                        # Read Player Coordinates
                        p_x = memory.read_float(player_obj_addr + offsets.OFFSET_POS_X)
                        p_y = memory.read_float(player_obj_addr + offsets.OFFSET_POS_Y)
                        p_z = memory.read_float(player_obj_addr + offsets.OFFSET_POS_Z)
                        p_rot = memory.read_float(player_obj_addr + offsets.OFFSET_ROTATION)

                        # print(f"Pos: {p_x:.1f}, {p_y:.1f}, {p_z:.1f} | HP: {current_health}/{max_health} | Target: {target_guid}")

                        # 4. Find Target Object (if we have a target)
                        if target_guid > 0:
                            target_obj_addr = find_object_by_guid(memory, client_conn_addr, target_guid)
                            if target_obj_addr:
                                target_descriptor_ptr = memory.read_int(target_obj_addr + offsets.OFFSET_DESCRIPTOR_PTR)
                                if target_descriptor_ptr:
                                    target_health = memory.read_int(target_descriptor_ptr + offsets.OFFSET_UNIT_HEALTH)
                                    target_max_health = memory.read_int(target_descriptor_ptr + offsets.OFFSET_UNIT_MAX_HEALTH)
                                    
                                    # Read Target Coordinates
                                    t_x = memory.read_float(target_obj_addr + offsets.OFFSET_POS_X)
                                    t_y = memory.read_float(target_obj_addr + offsets.OFFSET_POS_Y)
                                    
                                    # Calculate Angle and Turn
                                    target_angle = movement.calculate_angle(p_x, p_y, t_x, t_y)
                                    
                                    # Turn Logic
                                    # We now separate "Turning" from "Moving".
                                    # We can move AND turn if the angle is small.
                                    turn_direction = movement.get_turn_direction(p_rot, target_angle)
                                    
                                    if turn_direction:
                                        # Need to turn
                                        if turn_direction == 'left':
                                            input_handler.press_key('a', duration=0.05) # Short taps
                                        else:
                                            input_handler.press_key('d', duration=0.05)
                                            
                                    # Check distance
                                    dist = math.sqrt((t_x - p_x)**2 + (t_y - p_y)**2)
                                    
                                    # COMBAT CONFIGURATION
                                    ATTACK_RANGE = 25.0 # Set to 25.0 for Ranged/Caster!
                                    
                                    # Movement Logic
                                    # If we are far away, run.
                                    if dist > ATTACK_RANGE:
                                        # If the turn is VERY sharp (> 1.0 rad), stop moving to turn quickly.
                                        # Otherwise, keep running while turning.
                                        angle_diff = abs(target_angle - p_rot)
                                        if angle_diff > math.pi: angle_diff = 2*math.pi - angle_diff
                                        
                                        if angle_diff < 1.0: # ~60 degrees
                                            if not is_moving:
                                                print("   >>> Start Moving Forward...")
                                                input_handler.key_down('w')
                                                is_moving = True
                                        else:
                                            # Sharp turn, stop running
                                            if is_moving:
                                                input_handler.key_up('w')
                                                is_moving = False
                                    else:
                                        # In Range
                                        if is_moving:
                                            print("   >>> Stopping (In Range).")
                                            input_handler.key_up('w')
                                            is_moving = False
                                        
                                        # Attack Logic
                                        if target_health > 0:
                                            # print("   >>> Attacking...")
                                            input_handler.press_key('2')
                                        else:
                                            print("   >>> Target Dead.")
                                            
                                    if target_health <= 0 and is_moving:
                                         input_handler.key_up('w')
                                         is_moving = False

                            else:
                                print("   >>> Target object not found")
                                if is_moving:
                                    input_handler.key_up('w')
                                    is_moving = False
                        else:
                            # No target
                            if is_moving:
                                input_handler.key_up('w')
                                is_moving = False

                        # Auto-Heal Logic
                        if max_health > 0:
                            hp_percent = (current_health / max_health) * 100
                            if hp_percent < 50:
                                print(f"Health low ({hp_percent:.1f}%)! Using ability '1'...")
                                input_handler.press_key('1')
                    else:
                         print(f"Player Found: {hex(player_obj_addr)} | Descriptor invalid")
                else:
                    print(f"Player not found. GUID: {local_player_guid}")
                    if is_moving:
                        input_handler.key_up('w')
                        is_moving = False

                # Loop delay
                time.sleep(0.05) 
        except KeyboardInterrupt:
            print("Bot stopped.")
            try:
                input_handler.key_up('w')
            except: pass
    else:
        print("Could not attach to WoW. Make sure the game is running.")

if __name__ == "__main__":
    main()
