using System;

class MainApp {
	
	static void Main() {
		
		StupidClass boris = new StupidClass("Boris Nikolajevich",25);
		boris.introduce();
		
	}
	
}


public class StupidClass {
	
	public string name {get; set;}
	public int age {get; set;}
	
	public StupidClass(string name, int age) {
		
		this.name = name;
		this.age  = age;
		
	}
	
	public void introduce() {
		
		Console.WriteLine("Hi I am " + this.GetName() + " and I am " + this.GetAge() + " y.o.");
		
	}
	
	public string GetName() {
		
		return this.name;
		
	}
	
	public int GetAge() {
		
		return this.age;
		
	}
	
}