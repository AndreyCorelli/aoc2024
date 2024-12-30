using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

public class Computer
{
    private List<long> registers = new List<long> { 0L, 0L, 0L };
    private List<(long, long)> program = new List<(long, long)>();
    private string programString = "";
    private int pointer = 0;
    private List<long> output = new List<long>();

    public void ReadProgram(string filePath)
    {
        registers.Clear();
        foreach (var line in File.ReadLines(filePath))
        {
            var trimmedLine = line.Trim();
            if (trimmedLine.StartsWith("Register"))
            {
                registers.Add(int.Parse(trimmedLine.Split(": ")[1]));
            }
            else if (trimmedLine.StartsWith("Program: "))
            {
                programString = trimmedLine.Replace("Program: ", "").Trim();
                var numbers = programString.Split(',').Select(int.Parse).ToArray();
                for (int i = 0; i < numbers.Length; i += 2)
                {
                    program.Add((numbers[i], numbers[i + 1]));
                }
                break;
            }
        }
    }

    public void FindStartingValue(long startValue, long stopAt, CancellationToken cancellationToken)
    {
        long msgTillLog = 0;
        const long countBetweenLog = 1000000L;

        for (long i = startValue; i < stopAt; i++)
        {
            if (cancellationToken.IsCancellationRequested)
                return;

            msgTillLog--;
            if (msgTillLog < 0)
            {
                var progress = (int)(100 * (i - startValue) / (stopAt - startValue));
                Console.WriteLine($"Checking value: {i} ({progress}%)");
                msgTillLog = countBetweenLog - 1;
            }

            registers = new List<long> { (int)i, 0, 0 };
            if (ExecuteUntilOutputMatchesProgram())
            {
                Console.WriteLine($"Found starting value: {i}");
                throw new OperationCanceledException($"Value found: {i}");
            }
        }

        Console.WriteLine($"Nothing found between [{startValue}, {stopAt}]");
    }

    private bool ExecuteUntilOutputMatchesProgram()
    {
        pointer = 0;
        output.Clear();
        string outputStr = "";
        int lastOutputLength = 0;

        while (pointer >= 0 && pointer < program.Count)
        {
            long longPointer = PerformOperation(program[pointer]);

            if (longPointer < 0 || longPointer >= program.Count)
                return false;
            pointer = (int)longPointer;

            if (lastOutputLength < output.Count)
            {
                if (outputStr.Length > 0) outputStr += ",";
                outputStr += output.Last().ToString();

                if (!programString.StartsWith(outputStr))
                    return false;

                lastOutputLength = output.Count;
            }
        }

        return outputStr == programString;
    }

    private long PerformOperation((long, long) operation)
    {
        var (cmd, operand) = operation;
        var denominator = 0;

        switch (cmd)
        {
            case 0:
                denominator = (int)Math.Pow(2, GetComboOperand(operand));
                if (denominator == 0)
                    return -1;
                registers[0] /= denominator;
                return pointer + 1;
            case 1:
                registers[1] ^= operand;
                return pointer + 1;
            case 2:
                registers[1] = GetComboOperand(operand) % 8;
                return pointer + 1;
            case 3:
                return registers[0] != 0 ? operand : pointer + 1;
            case 4:
                registers[1] ^= registers[2];
                return pointer + 1;
            case 5:
                output.Add(GetComboOperand(operand) % 8);
                return pointer + 1;
            case 6:
                denominator = (int)Math.Pow(2, GetComboOperand(operand));
                if (denominator == 0)
                    return -1;
                registers[1] = registers[0] / denominator;
                return pointer + 1;
            case 7:
                denominator = (int)Math.Pow(2, GetComboOperand(operand));
                if (denominator == 0)
                    return -1;
                registers[2] = registers[0] / denominator;
                return pointer + 1;
            default:
                return pointer + 1;
        }
    }

    private long GetComboOperand(long operand)
    {
        return operand < 4 ? operand : registers[(int)operand - 4];
    }
}

public class Program
{
    private const string FilePath = "/Users/andreisitaev/sources/sennder/aoc2024/day17/input.txt";

    public static void Main()
    {
        long start = 0;
        long stop =  10000000000L * 4;

        var ranges = new List<(long, long)>();
        // split the start / stop in 4 ranges
        long step = (stop - start) / 4;
        for (long i = start; i < stop; i += step)
            ranges.Add((i, stop));

        Console.WriteLine("Starting parallel execution...");

        var cts = new CancellationTokenSource();
        var token = cts.Token;

        try
        {
            Parallel.ForEach(ranges, (range, state) =>
            {
                var computer = new Computer();
                computer.ReadProgram(FilePath);

                try
                {
                    Console.WriteLine($"Starting range: {range.Item1} - {range.Item2}");
                    computer.FindStartingValue(range.Item1, range.Item2, token);
                }
                catch (OperationCanceledException ex)
                {
                    Console.WriteLine(ex.Message);
                    cts.Cancel(); // Cancel all other tasks
                    state.Stop(); // Stop Parallel.ForEach immediately
                }
            });
        }
        catch (AggregateException)
        {
            // Exceptions are expected due to stopping execution
        }

        Console.WriteLine("Execution completed.");
    }
}
