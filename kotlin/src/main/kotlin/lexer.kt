package interpreter

import kotlin.text.StringBuilder


class Lexer(private val text: String) {
  private var pos: Int = 0

  fun GetNextToken(): Token {
    Skip()
    if (!HasNext()) {
      return Token(EOF)
    }

    return when {
      text[pos].isDigit() -> ReadInteger()
      text[pos] == '+' || text[pos] == '-' -> ReadOperator()
      else -> Error()
    }
  }

  private fun Skip() {
    while (HasNext() && text[pos] == ' ') {
      pos++;
    }
  }

  private fun ReadInteger(): IntegerToken {
    val sb = StringBuilder()
    while (HasNext() && text[pos].isDigit()) {
      sb.append(text[pos])
      pos++;
    }
    return IntegerToken(INTEGER, sb.toString().toInt())
  }

  private fun ReadOperator(): OperatorToken {
    val char = text[pos]
    pos++
    return when {
      char == '+' -> OperatorToken(PLUS, "+")
      char == '-' -> OperatorToken(MINUS, "-")
      else -> Error()
    }
  }

  private fun Error(): Nothing {
    throw Exception("Unexpected symbol.")
  }

  private fun HasNext() = pos < text.length
}
