from pymem import Pymem
from pymem.exception import ProcessNotFound

class MemoryReader:
    def __init__(self, process_name="Wow.exe"):
        self.process_name = process_name
        self.pm = None

    def attach(self):
        try:
            self.pm = Pymem(self.process_name)
            print(f"Attached to {self.process_name}")
            return True
        except ProcessNotFound:
            print(f"Process {self.process_name} not found.")
            return False
        except Exception as e:
            print(f"Error attaching to process: {e}")
            return False

    def read_int(self, address):
        if self.pm:
            try:
                return self.pm.read_int(address)
            except Exception as e:
                print(f"Error reading int at {hex(address)}: {e}")
        return None

    def read_float(self, address):
        if self.pm:
            try:
                return self.pm.read_float(address)
            except Exception as e:
                print(f"Error reading float at {hex(address)}: {e}")
        return None

    def read_ulong(self, address):
        """Reads an unsigned 64-bit integer (unsigned long long)."""
        if self.pm:
            try:
                return self.pm.read_ulonglong(address)
            except Exception as e:
                print(f"Error reading ulong at {hex(address)}: {e}")
        return None
    
    def read_uint(self, address):
        """Reads an unsigned 32-bit integer."""
        if self.pm:
            try:
                return self.pm.read_uint(address)
            except Exception as e:
                print(f"Error reading uint at {hex(address)}: {e}")
        return None
    
    def read_short(self, address):
        """Reads a 16-bit integer."""
        if self.pm:
            try:
                return self.pm.read_short(address)
            except Exception as e:
                print(f"Error reading short at {hex(address)}: {e}")
        return None

    def find_pattern(self, pattern):
        """
        Scans for a byte pattern.
        pattern: bytes (e.g., b'\\x90\\x90') or string regex if using pymem.pattern
        """
        if self.pm:
            try:
                # Pymem's pattern_scan_all usually takes bytes or a regex string.
                # For simplicity here we assume pymem's default behavior.
                # Note: exact implementation depends on pymem version features.
                import pymem.pattern
                return pymem.pattern.pattern_scan_all(self.pm.process_handle, pattern)
            except Exception as e:
                print(f"Error scanning pattern: {e}")
        return None

    def read_ptr_chain(self, base, offsets):
        """
        Reads a pointer chain.
        base: Initial static address.
        offsets: List of offsets to follow.
        Returns: The final address (not the value at that address).
        """
        if not self.pm: return None
        try:
            addr = self.read_int(base)
            for offset in offsets[:-1]:
                if not addr: return None
                addr = self.read_int(addr + offset)
            if not addr: return None
            return addr + offsets[-1]
        except Exception as e:
            print(f"Error reading pointer chain: {e}")
            return None
