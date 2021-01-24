// 2021.01.24
import kotlin.text.StringBuilder


typealias TokenType = String

val INTEGER: TokenType = "INTEGER"
val PLUS: TokenType = "PLUS"
val MINUS: TokenType = "MINUS"
val EOF: TokenType = "EOF"


data class Token(val type: TokenType, val value: Int?)


class Interpreter(
    private val input: String
  ) {

  private var currentToken: Token
  private var pos: Int = 0

  init {
    currentToken = getNextToken()
  }

  fun expr(): Int {
    val left = eat(INTEGER)
    val op = when {
      currentToken.type.equals(PLUS) -> eat(PLUS)
      currentToken.type.equals(MINUS) -> eat(MINUS)
      else -> error()
    }
    val right = eat(INTEGER)

    if (left.value == null || right.value == null) {
      throw Exception("Syntax error.")
    }
    return when {
      op.type.equals(PLUS) -> left.value + right.value
      op.type.equals(MINUS) -> left.value - right.value
      else -> error()
    }
  }

  private fun getNextToken(): Token {
    skip()
    val res = when {
      pos >= input.length -> Token(type=EOF, value=null)
      input[pos].isDigit() -> readInt()
      input[pos].equals('+') -> readOperator()
      input[pos].equals('-') -> readOperator()
      else -> Token(type=EOF, value=null)
    }
    return res
  }

  private fun nextChar() {
    pos++
  }

  private fun skip() {
    while (pos < input.length && input[pos] == ' ') {
      pos++
    }
  }

  private fun error(): Nothing {
    throw Exception("Syntax error.")
  }

  private fun readInt(): Token {
    val sb: StringBuilder = StringBuilder()
    while (pos < input.length && input[pos].isDigit()) {
      sb.append(input[pos])
      nextChar()
    }
    return Token(value=sb.toString().toInt(), type=INTEGER)
  }

  private fun readOperator(): Token {
    val res = when {
      input[pos] == '+' -> Token(type=PLUS, value=null)
      input[pos] == '-' -> Token(type=MINUS, value=null)
      else -> error()
    }
    nextChar()
    return res
  }

  private fun eat(tokenType: TokenType): Token {
    if (currentToken.type == tokenType) {
      val res = currentToken
      currentToken = getNextToken()
      return res
    }
    else {
      error()
    }
  }
}

fun Char.getIntValue() = this.toString().toInt()


fun printAnswer(n: Int, answer:  Int)  {
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
    val i = Interpreter(text)
    printAnswer(counter, i.expr())
    counter++
  }
}
