import java.util.*;

class Solution {

    private static final class RankedNumber {
        final int value;
        final int digitWeight;

        RankedNumber(int value) {
            this.value = value;
            this.digitWeight = digitWeightOf(value);
        }
    }

    public int minSwaps(int[] nums) {
        int n = nums.length;

        // Build the required final ordering independently of the input positions.
        RankedNumber[] targetOrder = new RankedNumber[n];
        for (int i = 0; i < n; i++) {
            targetOrder[i] = new RankedNumber(nums[i]);
        }

        Arrays.sort(targetOrder, (x, y) -> {
            int byDigitWeight = Integer.compare(x.digitWeight, y.digitWeight);
            if (byDigitWeight != 0) {
                return byDigitWeight;
            }
            return Integer.compare(x.value, y.value);
        });

        // Work on a private copy while tracking where every distinct value is.
        int[] current = nums.clone();
        Map<Integer, Integer> location = new HashMap<>(n * 2);

        for (int i = 0; i < n; i++) {
            location.put(current[i], i);
        }

        int swapCount = 0;

        // Fix positions from left to right. Whenever a position is wrong,
        // bring its required value directly from its current position.
        for (int slot = 0; slot < n; slot++) {
            int wanted = targetOrder[slot].value;

            if (current[slot] == wanted) {
                continue;
            }

            int source = location.get(wanted);
            int displaced = current[slot];

            current[slot] = wanted;
            current[source] = displaced;

            location.put(wanted, slot);
            location.put(displaced, slot);

            swapCount++;
        }

        return swapCount;
    }

    private static int digitWeightOf(int value) {
        int total = 0;

        while (value != 0) {
            total += value % 10;
            value /= 10;
        }

        return total;
    }
}