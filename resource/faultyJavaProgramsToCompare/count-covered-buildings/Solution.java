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
            if (x < minX[y])
                minX[y] = x;
            else if (x > maxX[y])
                maxX[y] = x;
            if (y < minY[x])
                minY[x] = y;
            else if (y > maxY[x])
                maxY[x] = y;
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