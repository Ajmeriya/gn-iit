"""
Multi-API Key Support with Automatic Rotation
Supports multiple Gemini API keys and rotates when quota is exceeded
"""

import os
from typing import List, Optional

class APIKeyManager:
    """
    Manages multiple Gemini API keys with automatic rotation on quota exceeded.
    """
    
    def __init__(self):
        self.keys: List[str] = []
        self.current_index = 0
        self.failed_keys = set()  # Track keys that hit quota limit
        
    def load_keys(self) -> List[str]:
        """
        Load API keys from environment variables.
        Supports: GEMINI_API_KEY, GEMINI_API_KEY_2, GEMINI_API_KEY_3, etc.
        """
        keys = []
        
        # Primary key
        primary_key = os.getenv("GEMINI_API_KEY")
        if primary_key:
            keys.append(primary_key)
        
        # Additional keys (GEMINI_API_KEY_2, GEMINI_API_KEY_3, ...)
        i = 2
        while True:
            key = os.getenv(f"GEMINI_API_KEY_{i}")
            if not key:
                break
            keys.append(key)
            i += 1
        
        self.keys = keys
        return keys
    
    def get_current_key(self) -> Optional[str]:
        """Get current active API key."""
        if not self.keys:
            self.load_keys()
        
        if not self.keys:
            return None
        
        return self.keys[self.current_index]
    
    def rotate_to_next(self) -> Optional[str]:
        """
        Rotate to next available API key.
        Returns None if all keys are exhausted.
        """
        if not self.keys:
            self.load_keys()
        
        if not self.keys:
            return None
        
        # Try next key
        start_index = self.current_index
        while True:
            self.current_index = (self.current_index + 1) % len(self.keys)
            
            # If we've tried all keys, return None
            if self.current_index == start_index:
                return None
            
            # Skip failed keys (quota exceeded)
            if self.current_index not in self.failed_keys:
                return self.keys[self.current_index]
        
        return None
    
    def mark_key_failed(self, key: Optional[str] = None):
        """
        Mark current key (or specified key) as failed due to quota.
        """
        if key is None:
            key = self.get_current_key()
        
        if key and key in self.keys:
            index = self.keys.index(key)
            self.failed_keys.add(index)
            print(f"⚠️  Marked API key {index + 1} as quota exceeded")
    
    def reset_failed_keys(self):
        """Reset all failed keys (useful after 24 hours)."""
        self.failed_keys.clear()
        print("✓ Reset failed keys - all keys available again")
    
    def get_available_keys_count(self) -> int:
        """Get count of available (non-failed) keys."""
        if not self.keys:
            self.load_keys()
        
        return len(self.keys) - len(self.failed_keys)
    
    def get_status(self) -> dict:
        """Get status of all keys."""
        if not self.keys:
            self.load_keys()
        
        return {
            "total_keys": len(self.keys),
            "available_keys": len(self.keys) - len(self.failed_keys),
            "failed_keys": len(self.failed_keys),
            "current_key_index": self.current_index,
            "failed_indices": list(self.failed_keys)
        }


# Global instance
_key_manager = None

def get_api_key_manager() -> APIKeyManager:
    """Get global API key manager instance."""
    global _key_manager
    if _key_manager is None:
        _key_manager = APIKeyManager()
        _key_manager.load_keys()
    return _key_manager

