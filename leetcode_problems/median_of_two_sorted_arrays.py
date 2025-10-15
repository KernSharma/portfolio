class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        min = 1000
        max = -1000
        lis = []
        for i in nums1:
            if i > max: max = i
            if i < min: min = i
        for i in nums2:
            if i > max: max = i
            if i < min: min = i
        for i in range(min, max):
            lis.append(i)
        if len(lis) % 2 == 1:
            return int(lis[len(lis)/2.0] + 1)
        else:
            return float((lis[(int(len(lis)/2))] + lis[int(len(lis)/2)+1])/2)
        
