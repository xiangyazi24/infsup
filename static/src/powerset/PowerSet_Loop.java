import java.util.Scanner;
import java.util.ArrayList;

public class PowerSet_Loop {
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


			int depth=0;
			while(depth<=i-1)
			{
				if (currentSet[i-1-depth]== n-depth)
				{
					depth++;
				}else{
					currentSet[i - 1 - depth]++;
					for (int j = i- depth; j < depth; j++)
					{
						currentSet[j] = currentSet[j - 1] + 1;
					}
					s.add(currentSet.clone());
					depth=0;
				}
				
			}
	
		}
		printSet(s);
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
