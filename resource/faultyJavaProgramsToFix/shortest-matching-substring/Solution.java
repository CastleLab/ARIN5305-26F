import java.util.Arrays;

class Solution {

    public int shortestMatchingSubstring(String s, String p) {
        Pieces pieces = parsePattern(p);

        int[] leftMatches = locateOccurrences(s, pieces.left);
        int[] middleMatches = locateOccurrences(s, pieces.middle);
        int[] rightMatches = locateOccurrences(s, pieces.right);

        int best = Integer.MAX_VALUE;

        for (int middleStart : middleMatches) {
            // The left part must finish no later than middleStart.
            int latestLeftIndex =
                    lastPositionAtMost(leftMatches, middleStart - pieces.left.length());

            if (latestLeftIndex < 0) {
                continue;
            }

            // The right part must begin no earlier than the end of the middle part.
            int firstRightIndex =
                    firstPositionAtLeast(
                            rightMatches,
                            middleStart + pieces.middle.length());

            if (firstRightIndex == rightMatches.length) {
                continue;
            }

            int windowStart = leftMatches[latestLeftIndex];
            int windowEnd =
                    rightMatches[firstRightIndex] + pieces.right.length();

            best = Math.min(best, windowEnd - windowStart);
        }

        return best == Integer.MAX_VALUE ? -1 : best;
    }

    private static int[] locateOccurrences(String text, String needle) {
        int n = text.length();

        if (needle.isEmpty()) {
            int[] everyBoundary = new int[n + 1];
            for (int i = 0; i <= n; i++) {
                everyBoundary[i] = i;
            }
            return everyBoundary;
        }

        int m = needle.length();
        String joined = needle + "#" + text;
        int[] z = buildZArray(joined);

        int[] buffer = new int[Math.max(0, n - m + 1)];
        int size = 0;

        for (int start = 0; start + m <= n; start++) {
            int joinedIndex = m + 1 + start;
            if (z[joinedIndex] >= m) {
                buffer[size++] = start;
            }
        }

        return Arrays.copyOf(buffer, size);
    }

    private static int[] buildZArray(String value) {
        int[] z = new int[value.length()];
        int left = 0;
        int right = -1;

        for (int i = 1; i < value.length(); i++) {
            if (i <= right) {
                z[i] = Math.min(right - i + 1, z[i - left]);
            }

            while (i + z[i] < value.length()
                    && value.charAt(z[i]) == value.charAt(i + z[i])) {
                z[i]++;
            }

            int reached = i + z[i];
            if (reached > right) {
                left = i;
                right = reached;
            }
        }

        return z;
    }

    private static int lastPositionAtMost(int[] sorted, int target) {
        int low = 0;
        int high = sorted.length;

        // Find the first value strictly greater than target.
        while (low < high) {
            int mid = low + (high - low) / 2;

            if (sorted[mid] <= target) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return low - 1;
    }

    private static int firstPositionAtLeast(int[] sorted, int target) {
        int low = 0;
        int high = sorted.length;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (sorted[mid] < target) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return low;
    }

    private static Pieces parsePattern(String pattern) {
        int firstWildcard = pattern.indexOf('*');
        int secondWildcard = pattern.indexOf('*', firstWildcard + 1);

        String left = pattern.substring(0, firstWildcard);
        String middle = pattern.substring(firstWildcard + 1, secondWildcard);
        String right = pattern.substring(secondWildcard + 1);

        return new Pieces(left, middle, right);
    }

    private static final class Pieces {
        final String left;
        final String middle;
        final String right;

        Pieces(String left, String middle, String right) {
            this.left = left;
            this.middle = middle;
            this.right = right;
        }
    }
}