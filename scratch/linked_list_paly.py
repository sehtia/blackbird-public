# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def to_array(self):
        result = [self.val]
        head = self.next
        while head:
            result.append(head.val)
            head = head.next
        return result


class Solution(object):

    def isPalindrome(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """
        reversed = self.reverse(head)
        print("head:", head.to_array())
        print("reversed:", reversed.to_array())
        while head:
            if head.val != reversed.val:
                return False
            head, reversed = head.next, reversed.next
        return True

    def get_midpoint(self, head):
        current_head = head
        size = 0
        while current_head:
            current_head = current_head.next
            size += 1
        midpoint = size / 2
        return int(midpoint)

    def reverse(self, head):
        new_head = None
        while head:
            new_head = ListNode(head.val, new_head)
            head = head.next
        return new_head


def main():
    node1 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(2, ListNode(1, None))))))
    solution = Solution()
    print("HWAT: ", solution.isPalindrome(node1))


if __name__ == "__main__":
    print("Sparking some good ish")
    main()
