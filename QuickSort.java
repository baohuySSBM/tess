import java.util.*;

public class QuickSort {

    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIdx = partition(arr, low, high);
            quickSort(arr, low, pivotIdx - 1);
            quickSort(arr, pivotIdx + 1, high);
        }
    }

    public static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {

            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        return i + 1;

    }

    public static void main(String[] args) {

        var nums = new int[] { 9, 4, 6, 2, 7, 5, 8, 1, 3 };
        var n = nums.length;

        System.out.printf("Before: %s\n", Arrays.toString(nums));
        quickSort(nums, 0, n - 1);
        System.out.printf("After: %s\n", Arrays.toString(nums));
    }

}
