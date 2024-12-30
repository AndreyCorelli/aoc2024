using System;
using System.Collections.Generic;
using System.IO;

public class Maze
{
    private char[,] matrix;
    private int width;
    private int height;
    private (int x, int y) start;
    private (int x, int y) end;
    private HashSet<string> disabledLeaps = new HashSet<string>();
    private readonly List<((int dx, int dy) intermediate, (int dx, int dy) final)> leapVectors = new()
    {
        ((0, 1), (0, 2)),
        ((0, -1), (0, -2)),
        ((1, 0), (2, 0)),
        ((-1, 0), (-2, 0))
    };
    private readonly List<(int dx, int dy)> moveVectors = new()
    {
        (0, 1), (0, -1), (1, 0), (-1, 0)
    };

    public long HighestCost { get; set; } = long.MaxValue;

    public Maze(string filePath)
    {
        ReadFromFile(filePath);
    }

    public int Solve(bool leapsAllowed)
    {
        var priorityQueue = new PriorityQueue<(int cost, (int x, int y) pos, string leapCoords), int>();
        var visited = new HashSet<string>();
        priorityQueue.Enqueue((0, start, "NO_CHEAT"), 0);

        while (priorityQueue.Count > 0)
        {
            var (cost, (x, y), leapCoords) = priorityQueue.Dequeue();
            if (cost > HighestCost) continue;

            if ((x, y) == end)
            {
                if (leapCoords != "NO_CHEAT")
                {
                    disabledLeaps.Add(leapCoords);
                }
                return cost;
            }

            foreach (var (dx, dy) in moveVectors)
            {
                int nx = x + dx, ny = y + dy;
                if (IsWithinBounds(nx, ny) && matrix[ny, nx] == '.')
                {
                    string key = $"{nx},{ny}:{leapCoords}";
                    if (!visited.Contains(key))
                    {
                        priorityQueue.Enqueue((cost + 1, (nx, ny), leapCoords), cost + 1);
                        visited.Add(key);
                    }
                }
            }

            if (leapsAllowed && leapCoords == "NO_CHEAT")
            {
                foreach (var ((dx1, dy1), (dx2, dy2)) in leapVectors)
                {
                    int nx = x + dx2, ny = y + dy2;
                    int mx = x + dx1, my = y + dy1;

                    if (IsWithinBounds(nx, ny) && IsWithinBounds(mx, my) &&
                        matrix[my, mx] == '#' && matrix[ny, nx] == '.')
                    {
                        string newLeapCoords = $"{x},{y}->{nx},{ny}";
                        if (!disabledLeaps.Contains(newLeapCoords))
                        {
                            string key = $"{nx},{ny}:{newLeapCoords}";
                            if (!visited.Contains(key))
                            {
                                priorityQueue.Enqueue((cost + 2, (nx, ny), newLeapCoords), cost + 2);
                                visited.Add(key);
                            }
                        }
                    }
                }
            }
        }

        return -1;
    }

    private void ReadFromFile(string filePath)
    {
        var lines = File.ReadAllLines(filePath);
        height = lines.Length;
        width = lines[0].Length;
        matrix = new char[height, width];

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                char c = lines[y][x];
                matrix[y, x] = c;

                if (c == 'S')
                {
                    start = (x, y);
                    matrix[y, x] = '.';
                }
                else if (c == 'E')
                {
                    end = (x, y);
                    matrix[y, x] = '.';
                }
            }
        }
    }

    private bool IsWithinBounds(int x, int y)
    {
        return x >= 0 && x < width && y >= 0 && y < height;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        if (args.Length != 1)
        {
            Console.WriteLine("Usage: MazeSolver <input file path>");
            return;
        }

        string filePath = args[0];
        var maze = new Maze(filePath);

        int baseCost = maze.Solve(false);
        maze.HighestCost = baseCost - 100;
        Console.WriteLine($"\nBase cost: {baseCost}");

        int counter = 0;
        while (true)
        {
            int cheatCost = maze.Solve(true);
            if (cheatCost == -1) break;

            counter++;
            int cheatProfit = baseCost - cheatCost;
            Console.WriteLine($"[{counter}] Cheating profit: {cheatProfit}");

            if (cheatProfit < 5 || counter > 755) break;
        }

        Console.WriteLine("Done");
    }
}
