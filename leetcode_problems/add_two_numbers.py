class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        carry = 0
        dummyHead = ListNode(0)
        currentNode = dummyHead
        while l1 is not None or l2 is not None or carry != 0:
            if l1 is not None:
              val1 = l1.val 
            else:
              val1 = 0
            if l2 is not None:
              val2 = l2.val 
            else:
              val2 = 0
            total_sum = val1 + val2 + carry
            new_digit = total_sum % 10
            carry = total_sum // 10
            new_node = ListNode(new_digit)
            currentNode.next = new_node
            currentNode = currentNode.next
            if l1 is not None:
              l1 = l1.next 
            else: 
              l1 = None
            if l2 is not None:
              l2 = l2.next 
            else:
              l2 = None

        return dummyHead.next


