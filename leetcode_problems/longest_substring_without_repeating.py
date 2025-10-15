class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        current_substring = []
        max_length = 0
        
        for char in s:
            if char in current_substring:
                index = current_substring.index(char)
                current_substring = current_substring[index + 1:]
            
            current_substring.append(char)
            max_length = max(max_length, len(current_substring))
            
        return max_length
