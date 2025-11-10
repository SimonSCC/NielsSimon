
using Microsoft.AspNetCore.SignalR.Client;

Console.WriteLine("SignalR Console Chat Client");
Console.Write("Enter your name: ");
string user = Console.ReadLine() ?? "User";

var connection = new HubConnectionBuilder()
    .WithUrl("http://localhost:5285/chat")
    .WithAutomaticReconnect()
    .Build();

connection.On<string, string>("ReceiveMessage", (sender, message) =>
{
    var prevColor = Console.ForegroundColor;
    Console.ForegroundColor = ConsoleColor.Green;
    Console.WriteLine($"{sender}: {message}");
    Console.ForegroundColor = prevColor;
});

await connection.StartAsync();
Console.WriteLine("Connected! Type messages and press Enter. Type /exit to quit.");

string? input;
while ((input = Console.ReadLine()) != "/exit")
{
    if (!string.IsNullOrWhiteSpace(input))
    {
        await connection.InvokeAsync("SendMessage", user, input);
    }
}

await connection.StopAsync();
Console.WriteLine("Disconnected.");

// Game/game logic below can be restored or integrated as needed.

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