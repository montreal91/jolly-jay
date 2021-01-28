package interpreter

import org.junit.Test
import org.junit.Ignore
import org.junit.Assert.assertEquals


class LexerTest {
  @Test
  fun TestInteger(): Unit {
    val lexer = MakeLexer("42")
    val token = lexer.GetNextToken()
    CheckToken(token, INTEGER, 42)
  }

  @Test
  fun TestEndOfLine() {
    val lexer = MakeLexer("")
    val token = lexer.GetNextToken()
    CheckToken(token, EOF, -1)
  }

  @Test
  fun TestPlus() {
    val lexer = MakeLexer("+")
    val token = lexer.GetNextToken()
    CheckToken(token, PLUS, "+")
  }

  @Test
  fun TestMinus() {
    val lexer = MakeLexer("-")
    val token = lexer.GetNextToken()
    CheckToken(token, MINUS, "-")
  }

  @Test
  fun TestExpression() {
    val lexer = MakeLexer("1 + 2 - 3")

    var token: Token = lexer.GetNextToken()
    CheckToken(token, INTEGER, 1)

    token = lexer.GetNextToken()
    CheckToken(token, PLUS, "+")

    token = lexer.GetNextToken()
    CheckToken(token, INTEGER, 2)

    token = lexer.GetNextToken()
    CheckToken(token, MINUS, "-")

    token = lexer.GetNextToken()
    CheckToken(token, INTEGER, 3)

    token = lexer.GetNextToken()
    CheckToken(token, EOF, 0)
  }
}


private fun MakeLexer(text: String) = Lexer(text)

private fun CheckToken(
    token: Token, expectedType: TokenType, expectedValue: Any
) {
  assertEquals(expectedType, token.GetType())
  when (token) {
    is IntegerToken -> assertEquals(expectedValue, token.GetValue())
    is OperatorToken -> assertEquals(expectedValue, token.GetValue())
    else -> {}
  }
}
