import java.util.*;

class Solution {
    private static final int[][] STEP = {
        {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    private static final class State {
        final int cell;
        final int cleaned;
        final int power;

        State(int cell, int cleaned, int power) {
            this.cell = cell;
            this.cleaned = cleaned;
            this.power = power;
        }
    }

    public int minMoves(String[] classroom, int energy) {
        final int height = classroom.length;
        final int width = classroom[0].length();
        final int cells = height * width;

        char[][] room = new char[height][];
        int[] litterBit = new int[cells];

        int start = -1;
        int litterCount = 0;

        for (int r = 0; r < height; r++) {
            room[r] = classroom[r].toCharArray();

            for (int c = 0; c < width; c++) {
                int id = r * width + c;

                switch (room[r][c]) {
                    case 'S' -> start = id;
                    case 'L' -> litterBit[id] = 1 << litterCount++;
                    default -> { }
                }
            }
        }

        final int allClean = (1 << litterCount) - 1;

        /*
         * strongest[mask][cell] records the greatest remaining
         * energy seen for this cleaned-litter set at this cell.
         */
        int[][] strongest = new int[1 << litterCount][cells];

        ArrayDeque<State> frontier = new ArrayDeque<>();

        frontier.addLast(new State(start, 0, energy));
        strongest[0][start] = energy;

        int moves = 0;

        while (!frontier.isEmpty()) {
            int levelSize = frontier.size();

            while (levelSize-- > 0) {
                State cur = frontier.removeFirst();

                if (cur.cleaned == allClean) {
                    return moves;
                }

                /*
                 * A state reaching the same (cell, mask) with more
                 * energy dominates this state.
                 */
                if (cur.power < strongest[cur.cleaned][cur.cell]
                        || cur.power == 0) {
                    continue;
                }

                int r = cur.cell / width;
                int c = cur.cell % width;

                for (int[] d : STEP) {
                    int nr = r + d[0];
                    int nc = c + d[1];

                    if (!inside(nr, nc, height, width)
                            || room[nr][nc] == 'X') {
                        continue;
                    }

                    int nextCell = nr * width + nc;

                    int nextMask =
                            cur.cleaned | litterBit[nextCell];

                    int nextPower =
                            room[nr][nc] == 'R'
                                    ? energy
                                    : cur.power - 1;

                    if (nextPower <= strongest[nextMask][nextCell]) {
                        continue;
                    }

                    strongest[nextMask][nextCell] = nextPower;

                    frontier.addLast(
                            new State(nextCell, nextMask, nextPower)
                    );
                }
            }

            moves++;
        }

        return -1;
    }

    private static boolean inside(
            int r, int c, int height, int width) {
        return r >= 0
                && r < height
                && c >= 0
                && c < width;
    }
}