import java.util.ArrayList;
import java.util.List;

public class Solution {
    public int minMoves(String[] classroom, int energy) {
        int m = classroom.length, n = classroom[0].length();

        int[][] litterId = new int[m][n];
        int startRow = 0, startCol = 0, litterCount = 0;

        for (int i = 0; i < m; i++) {
            String row = classroom[i];
            for (int j = 0; j < n; j++) {
                char cell = row.charAt(j);
                if (cell == 'S') {
                    startRow = i;
                    startCol = j;
                } else if (cell == 'L') {
                    litterId[i][j] = litterCount++;
                }
            }
        }

        if (litterCount == 0) {
            return 0;
        }

        int fullMask = (1 << litterCount) - 1;
        boolean[][][][] visited =
                new boolean[m][n][energy + 1][1 << litterCount];

        List<int[]> queue = new ArrayList<>();
        queue.add(new int[]{startRow, startCol, energy, fullMask});
        visited[startRow][startCol][energy][fullMask] = true;

        int[] dirs = {-1, 0, 1, 0, -1};
        int moves = 0;

        while (!queue.isEmpty()) {
            List<int[]> currentLevel = queue;
            queue = new ArrayList<>();

            for (int[] state : currentLevel) {
                int row = state[0];
                int col = state[1];
                int remainingEnergy = state[2];
                int mask = state[3];

                if (mask == 0) {
                    return moves;
                }

                for (int k = 0; k < 4; k++) {
                    int nr = row + dirs[k];
                    int nc = col + dirs[k + 1];

                    if (nr < 0 || nr >= m || nc < 0 || nc >= n) {
                        continue;
                    }

                    char cell = classroom[nr].charAt(nc);
                    if (cell == 'X') {
                        continue;
                    }

                    int nextEnergy = remainingEnergy - 1;
                    if (cell == 'R') {
                        nextEnergy = energy;
                    }
                    if (nextEnergy < 0) {
                        continue;
                    }

                    int nextMask = mask;
                    if (cell == 'L') {
                        nextMask &= ~(1 << litterId[nr][nc]);
                    }

                    if (!visited[nr][nc][nextEnergy][nextMask]) {
                        visited[nr][nc][nextEnergy][nextMask] = true;
                        queue.add(new int[]{nr, nc, nextEnergy, nextMask});
                    }
                }
            }

            moves++;
        }

        return -1;
    }
}