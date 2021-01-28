package main

import interpreter.MakeInterpreter


fun PrintAnswer(n: Int, answer:  Int)  {
  println("Out[$n]: $answer\n")
}


fun main() {
  println("Write 'q' to quit.")
  var counter = 1
  while (true) {
    print("In [$counter]: ")
    val text: String = readLine()!!
    if (text.equals("q")){
      break
    }
    val i = MakeInterpreter(text)
    PrintAnswer(counter, i.Execute())
    counter++
  }
}
