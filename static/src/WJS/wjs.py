# import typing
from typing import List
# import bisect_right
from bisect import bisect_right


class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs, dp = sorted([(e, s, p) for e, s, p in zip(endTime, startTime, profit)]), [
            0] * (len(startTime))
        jobs_by_start = sorted([(s, index)
                                for index, (e, s, p) in enumerate(jobs)])
        # print(jobs_by_start)
        P = [0] * (len(startTime))

        self.pred(jobs, jobs_by_start, P)

        # print(P)
        dp[0] = jobs[0][2]
        for i in range(1, len(jobs)):
            dp[i] = max(
                dp[P[i]] + jobs[i][2],
                dp[i - 1]
            )
        return dp[-1]

    def pred(self, ends, starts, P):
        i = 0
        j = 0
        while i < len(ends) and j < len(starts):
            if ends[i][0] <= starts[j][0]:
                i += 1
            else:
                # we might want to do i-1, if we want things starting from 0
                P[starts[j][1]] = i - 1
                j += 1
