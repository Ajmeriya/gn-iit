"""
Reference Solver: Linked List Pattern
Handles problems like Reverse Linked List, Merge Lists, Detect Cycle, etc.
"""

from typing import List, Dict, Any, Optional

class ListNode:
    """Simple ListNode class for reference solver"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def solve_linked_list(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Linked List pattern"""
    if problem_type == "reverse_list":
        head = _list_to_linked_list(inputs.get("values", []))
        reversed_head = _reverse_list(head)
        return _linked_list_to_list(reversed_head)
    
    elif problem_type == "merge_lists":
        list1 = _list_to_linked_list(inputs.get("list1", []))
        list2 = _list_to_linked_list(inputs.get("list2", []))
        merged = _merge_lists(list1, list2)
        return _linked_list_to_list(merged)
    
    elif problem_type == "has_cycle":
        values = inputs.get("values", [])
        pos = inputs.get("pos", -1)  # -1 means no cycle
        head = _list_to_linked_list_with_cycle(values, pos)
        return _has_cycle(head)
    
    elif problem_type == "remove_nth":
        values = inputs.get("values", [])
        n = inputs.get("n", 0)
        head = _list_to_linked_list(values)
        new_head = _remove_nth(head, n)
        return _linked_list_to_list(new_head)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _list_to_linked_list(values: List[int]) -> Optional[ListNode]:
    """Convert list to linked list"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head

def _list_to_linked_list_with_cycle(values: List[int], pos: int) -> Optional[ListNode]:
    """Convert list to linked list with optional cycle"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    nodes = [head]
    
    for val in values[1:]:
        node = ListNode(val)
        current.next = node
        current = node
        nodes.append(node)
    
    if 0 <= pos < len(nodes):
        current.next = nodes[pos]
    
    return head

def _linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Convert linked list to list"""
    result = []
    current = head
    visited = set()
    
    while current:
        if id(current) in visited:  # Cycle detection
            break
        visited.add(id(current))
        result.append(current.val)
        current = current.next
    
    return result

def _reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse Linked List"""
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev

def _merge_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """Merge Two Sorted Lists"""
    dummy = ListNode(0)
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    current.next = list1 if list1 else list2
    return dummy.next

def _has_cycle(head: Optional[ListNode]) -> bool:
    """Linked List Cycle: Detect if cycle exists"""
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    
    return False

def _remove_nth(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """Remove Nth Node From End"""
    dummy = ListNode(0)
    dummy.next = head
    
    first = dummy
    second = dummy
    
    for _ in range(n + 1):
        first = first.next
    
    while first:
        first = first.next
        second = second.next
    
    second.next = second.next.next
    return dummy.next

