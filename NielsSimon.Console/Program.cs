// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");

Console.WriteLine("Ctrl+ shift + P opens the command palette.");

Game game = new Game();
game.Start();

public class Game
{
    public int DayCount = 0;
    public Player Niels = new Player();

    public void Start()
    {
        Console.WriteLine("Game started. Press Ctrl+C to exit.");
        while (true)
        {
            // Class Method Input Type
            string? inputFromConsole = Console.ReadLine();
            Console.WriteLine("Input received: " + inputFromConsole);

            switch (inputFromConsole?.ToLower())
            {
                case "nextday":
                    DayCount++;
                    Console.WriteLine($"It's {DayCount} day(s) into the game.");
                    break;

                //Lav en case "money" der printer spillerens penge ud
                case "money":
                    Niels.PrintMoney();
                    break;

                case "buyhouse":
                    House newHouse = new House();
                    newHouse.Buy(Niels);
                    break;

                default:
                    Console.WriteLine("It's just another day.");
                    break;
            }
        }
    }
}

public class Player
{
    public int Money = 100;
    public List<House> Houses = new List<House>();

    public void PrintMoney()
    {
        Console.WriteLine("You have " + Money + " money.");
    }

}

public class House
{
    public int Price = 10;
    private int Income = 5;

    public List<Decoration> AvailabeDecorations = new List<Decoration>(){
        new Decoration("Basic Furniture", 5, 2),
        new Decoration("Garden", 10, 3)
    };

    public List<Decoration> Decorations = new List<Decoration>();

    public void Buy(Player player)
    {
        if (player.Money >= Price)
        {
            player.Money -= Price;
            Console.WriteLine("House bought!");
            player.Houses.Add(this);
        }
        else
        {
            Console.WriteLine("Not enough money to buy the house.");
        }
    }
}

public class Decoration
{
    public string Name;
    public int Cost;
    public int ExtraIncome;

    public Decoration(string name, int cost, int extraIncome)
    {
        Name = name;
        Cost = cost;
        ExtraIncome = extraIncome;
    }
}