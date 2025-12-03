class Solution:
    def romanToInt(self, s: str) -> int:
        """
        Convert Roman numeral to integer.
        
        Key Insight:
        - Normally add values
        - If current < next → subtract (e.g., IV → subtract I)
        
        Plan:
        1. Create mapping dictionary
        2. Traverse from left to right
        3. Compare current and next symbol
        """
        # TODO: Define roman to int mapping
        # TODO: Initialize total = 0
        # TODO: Loop through string with proper condition
        roman = {
            'I': 1, 'V': 5, 'X': 10, 'L': 50,
            'C': 100, 'D': 500, 'M': 1000
        }

        
        for ch in s:
            if ch not in roman:
                print("Invalid Entry! Only Roman characters ROMAN NUMBERS are allowed.")
                return None
        

        total = 0
        for i in range(len(s)):
            if i + 1 < len(s) and roman[s[i]] < roman[s[i + 1]]:
                total -= roman[s[i]]
            else:
                total += roman[s[i]]

        return total



user_ip = input("Enter a Roman numeral: ")
solver = Solution()
result = solver.romanToInt(user_ip)
if result is not None:
    print(result)
