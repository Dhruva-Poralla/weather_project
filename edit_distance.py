def edit_distance(s1, s2):
    """
    Calculate the minimum number of operations required to convert string s1 to string s2.
    
    Operations allowed:
    1. Deletion of a character
    2. Replacement of a character with another one
    3. Insertion of a character
    
    Args:
        s1 (str): Source string
        s2 (str): Target string
    
    Returns:
        int: Minimum number of operations required
    """
    m, n = len(s1), len(s2)
    
    # Create a DP table to store the minimum operations
    # dp[i][j] represents the minimum operations to convert s1[0:i] to s2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    # Converting empty string to s2 requires j insertions
    for j in range(n + 1):
        dp[0][j] = j
    
    # Converting s1 to empty string requires i deletions
    for i in range(m + 1):
        dp[i][0] = i
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i-1][j-1]
            else:
                # Characters don't match, consider all three operations:
                # 1. Deletion: dp[i-1][j] + 1 (remove character from s1)
                # 2. Insertion: dp[i][j-1] + 1 (add character to s1)
                # 3. Replacement: dp[i-1][j-1] + 1 (replace character in s1)
                dp[i][j] = 1 + min(dp[i-1][j],      # deletion
                                  dp[i][j-1],       # insertion
                                  dp[i-1][j-1])     # replacement
    
    return dp[m][n]


def edit_distance_optimized(s1, s2):
    """
    Space-optimized version of edit distance using only O(min(m,n)) space.
    """
    m, n = len(s1), len(s2)
    
    # Ensure s1 is the shorter string to optimize space
    if m > n:
        s1, s2 = s2, s1
        m, n = n, m
    
    # Use only two rows for DP
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        curr[0] = j
        for i in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                curr[i] = prev[i-1]
            else:
                curr[i] = 1 + min(prev[i],      # deletion
                                 curr[i-1],     # insertion
                                 prev[i-1])     # replacement
        prev, curr = curr, prev
    
    return prev[m]


def print_operations(s1, s2):
    """
    Print the sequence of operations to convert s1 to s2.
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    # Backtrack to find operations
    operations = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j-1] + 1:
            operations.append(f"Replace '{s1[i-1]}' with '{s2[j-1]}' at position {i-1}")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j] + 1:
            operations.append(f"Delete '{s1[i-1]}' at position {i-1}")
            i -= 1
        else:
            operations.append(f"Insert '{s2[j-1]}' at position {i}")
            j -= 1
    
    while i > 0:
        operations.append(f"Delete '{s1[i-1]}' at position {i-1}")
        i -= 1
    
    while j > 0:
        operations.append(f"Insert '{s2[j-1]}' at position {i}")
        j -= 1
    
    operations.reverse()
    return operations


# Test cases
if __name__ == "__main__":
    # Test case from the problem: "horse" -> "ros"
    s1, s2 = "horse", "ros"
    result = edit_distance(s1, s2)
    print(f"Edit distance from '{s1}' to '{s2}': {result}")
    
    # Print the operations
    operations = print_operations(s1, s2)
    print("Operations:")
    for i, op in enumerate(operations, 1):
        print(f"  Step {i}: {op}")
    
    print()
    
    # Additional test cases
    test_cases = [
        ("kitten", "sitting"),
        ("", "abc"),
        ("abc", ""),
        ("abc", "abc"),
        ("intention", "execution"),
        ("sunday", "saturday")
    ]
    
    for s1, s2 in test_cases:
        result = edit_distance(s1, s2)
        print(f"Edit distance from '{s1}' to '{s2}': {result}")
    
    print("\nTesting optimized version:")
    for s1, s2 in test_cases:
        result_opt = edit_distance_optimized(s1, s2)
        result_orig = edit_distance(s1, s2)
        print(f"Optimized: {result_opt}, Original: {result_orig}, Match: {result_opt == result_orig}")