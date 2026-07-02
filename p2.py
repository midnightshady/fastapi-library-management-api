nums = [1,3,4,2,2]

slow = nums[0]
fast = nums[0]

while fast < len(nums):

    slow = nums[slow]
    fast = nums[nums[fast]]

    if slow == fast:
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        print(True)

print(False)