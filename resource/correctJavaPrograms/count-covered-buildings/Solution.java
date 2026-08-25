import java.util.Arrays;

public class Solution {
    public int countCoveredBuildings(int n, int[][] buildings) {
        int[] minX = new int[n + 1];
        int[] maxX = new int[n + 1];
        int[] minY = new int[n + 1];
        int[] maxY = new int[n + 1];

        Arrays.fill(minX, n + 1);
        Arrays.fill(minY, n + 1);

        for (int[] building : buildings) {
            final int x = building[0];
            final int y = building[1];
            minX[y] = Math.min(minX[y], x);
            maxX[y] = Math.max(maxX[y], x);
            minY[x] = Math.min(minY[x], y);
            maxY[x] = Math.max(maxY[x], y);
        }

        int ans = 0;

        for (int[] building : buildings) {
            final int x = building[0];
            final int y = building[1];
            if (minX[y] < x && x < maxX[y] &&
                    minY[x] < y && y < maxY[x])
                ++ans;
        }

        return ans;
    }
}