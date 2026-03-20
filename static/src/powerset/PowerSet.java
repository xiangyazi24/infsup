import java.util.Scanner;
import java.util.ArrayList;

public class PowerSet {
	private static int n;
	private static Scanner scan;
	public static void main(String[] args)
	{
		//Get User Input
		scan = new Scanner(System.in);
		System.out.println("Enter number between 1 and 20");
		n = scan.nextInt();
		
		//Use Backtracking Algorithm
		ArrayList<int[]> s = new ArrayList<int[]>();
		int[] currentSet;
		for (int i = 1; i <= n; i ++)
		{
			currentSet = new int[i];
			for (int j = 1; j <= i; j++)
			{
				currentSet[j - 1] = j;
			}
			s.add(currentSet.clone());
			nextSet(currentSet, 0, s);
	
		}
		printSet(s);
	}
	public static void nextSet(int[] lastSet, int depth, ArrayList<int[]> s)
	{   int len=lastSet.length;
		// too deep
		if(depth > len-1) return;
		// can not continue with current level, go deeper
		if(lastSet[len - 1 -depth] == n-depth)
		{
			nextSet(lastSet, depth+1,s);
		}
		else{
			lastSet[len - 1 - depth]++;
			for (int i = len- depth; i < depth; i++)
			{
				lastSet[i] = lastSet[i - 1] + 1;
			}
			s.add(lastSet.clone());
			nextSet(lastSet, 0,s);
		}

		
	}
	
	
	
	//Print methods
	public static void printArray(int[] array)
	{
		System.out.print("{");
		for (int i = 0; i < array.length; i++)
		{
			System.out.print(array[i]);
			if (i < array.length - 1)
			{
				System.out.print(", ");
			}
		}
		System.out.print("}\n");;
	}
	public static void printSet(ArrayList<int[]> s)
	{
		System.out.println("{E,");
		for (int i = 0; i < s.size(); i++)
		{
			printArray(s.get(i));
			if (i < s.size() - 1)
			{
				System.out.println(",");
			}
		}
		System.out.print("}");
	}
}
