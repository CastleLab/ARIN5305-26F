import java.util.Arrays;
import java.util.Comparator;

class Solution {

    private static final int VERTICAL = 0x01, HORIZONTAL = 0x03;

    private static final class Site {
        final int x;
        final int y;
        int surrounded;

        Site(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }

    public int countCoveredBuildings(int n, int[][] buildings) {
        Site[] sites = new Site[buildings.length];

        for (int i = 0; i < buildings.length; i++) {
            sites[i] = new Site(buildings[i][0], buildings[i][1]);
        }

        // In a same-x run sorted by y, every non-endpoint building
        // has another building both above and below it.
        Arrays.sort(
            sites,
            Comparator.comparingInt((Site s) -> s.x)
                      .thenComparingInt(s -> s.y)
        );
        markInteriorOfRuns(sites, true, VERTICAL);

        // In a same-y run sorted by x, every non-endpoint building
        // has another building both left and right of it.
        Arrays.sort(
            sites,
            Comparator.comparingInt((Site s) -> s.y)
                      .thenComparingInt(s -> s.x)
        );
        markInteriorOfRuns(sites, false, HORIZONTAL);

        int covered = 0;
        for (Site site : sites) {
            if (site.surrounded == (VERTICAL | HORIZONTAL)) {
                covered++;
            }
        }
        return covered;
    }

    private void markInteriorOfRuns(
        Site[] sites,
        boolean groupByX,
        int directionFlag
    ) {
        int first = 0;

        while (first < sites.length) {
            int key = groupByX ? sites[first].x : sites[first].y;
            int afterLast = first + 1;

            while (afterLast < sites.length) {
                int nextKey = groupByX
                    ? sites[afterLast].x
                    : sites[afterLast].y;

                if (nextKey != key) {
                    break;
                }
                afterLast++;
            }

            // first and afterLast - 1 are extrema of this row/column.
            for (int i = first + 1; i < afterLast - 1; i++) {
                sites[i].surrounded |= directionFlag;
            }

            first = afterLast;
        }
    }
}