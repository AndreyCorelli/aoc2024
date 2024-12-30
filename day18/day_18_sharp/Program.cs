using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class MemoryMap
{
    private int Width { get; set; }
    private int Height { get; set; }
    private (int, int) Start { get; set; }
    private (int, int) End { get; set; }
    private List<(int, int)> ByteCoords { get; set; }
    private List<List<char>> Matrix { get; set; }

    private static readonly Dictionary<string, (string Path, (int Width, int Height) Size)> INPUT = new()
    {
        { "normal", ("/Users/andreisitaev/sources/sennder/aoc2024/day18/input.txt", (71, 71)) }
    };

    public MemoryMap(string inputKey)
    {
        (string path, (int width, int height) size) = INPUT[inputKey];
        Width = size.Item1;
        Height = size.Item2;
        Start = (0, 0);
        End = (Width - 1, Height - 1);
        ByteCoords = new List<(int, int)>();
        Matrix = new List<List<char>>();

        ReadFile(path);
    }

    public bool Solve(int bytesLimit)
    {
        BuildMatrix(bytesLimit);
        bool wasFound = FindPath();
        if (!wasFound)
        {
            Console.WriteLine($"Path wasn't found, last byte: {ByteCoords[bytesLimit - 1]}");
        }
        return wasFound;
    }

    public void Print()
    {
        if (Matrix.Count == 0)
        {
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    Console.Write(ByteCoords.Contains((x, y)) ? "#" : ".");
                }
                Console.WriteLine();
            }
        }
        else
        {
            foreach (var row in Matrix)
            {
                Console.WriteLine(string.Concat(row));
            }
        }
    }

    private bool FindPath()
    {
        var visited = new Dictionary<(int, int), int>();
        var stack = new PriorityQueue<(int Length, (int X, int Y) Coords), int>();
        stack.Enqueue((0, Start), 0);

        while (stack.Count > 0)
        {
            var (length, coords) = stack.Dequeue();
            if (coords == End)
            {
                return true;
            }

            if (visited.ContainsKey(coords) && visited[coords] <= length)
            {
                continue;
            }

            visited[coords] = length;
            var (x, y) = coords;
            foreach (var (xOffset, yOffset) in new[] { (0, 1), (0, -1), (1, 0), (-1, 0) })
            {
                int newX = x + xOffset;
                int newY = y + yOffset;
                if (newX >= 0 && newX < Width && newY >= 0 && newY < Height && Matrix[newY][newX] == '.')
                {
                    stack.Enqueue((length + 1, (newX, newY)), length + 1);
                }
            }
        }

        return false;
    }

    private void BuildMatrix(int bytesLimit)
    {
        Matrix = new List<List<char>>();
        var selectedBytes = new HashSet<(int, int)>(ByteCoords.Take(bytesLimit));
        for (int y = 0; y < Height; y++)
        {
            var row = new List<char>();
            for (int x = 0; x < Width; x++)
            {
                row.Add(selectedBytes.Contains((x, y)) ? '#' : '.');
            }
            Matrix.Add(row);
        }
    }

    private void ReadFile(string path)
    {
        foreach (var line in File.ReadLines(path))
        {
            var parts = line.Trim().Split(',');
            int x = int.Parse(parts[0]);
            int y = int.Parse(parts[1]);
            ByteCoords.Add((x, y));
        }
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        var memoryMap = new MemoryMap("normal");
        var startTime = DateTime.Now;
        for (int i = 1024; i < 99999; i++)
        {
            if (!memoryMap.Solve(i))
            {
                break;
            }
        }
        var elapsed = (DateTime.Now - startTime).TotalSeconds;
        Console.WriteLine($"Elapsed: {elapsed}s");
    }
}
