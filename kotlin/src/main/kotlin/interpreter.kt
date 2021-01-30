package interpreter


class Interpreter(private val lexer: Lexer) {
  private var currentToken: Token = lexer.GetNextToken()

  //
  // Execute arithmetic expression
  //
  // IN : (561 - 5 * (52 + 59)) * (28 - 21)
  // OUT: 42
  //
  fun Execute(): Int = Expr()

  //
  // Process expr rule
  //
  // expr    : operand ((PLUS | MINUS) operand) *
  // operand : factor ((MUL | DIV) factor) *
  // factor  : INTEGER | LPAR expr RPAR
  //
  private fun Expr(): Int {
    var left = Operand()

    while (currentToken.GetType() == PLUS || currentToken.GetType() == MINUS) {
      val op = currentToken
      when {
        op.GetType().equals(PLUS) -> Eat(PLUS)
        op.GetType().equals(MINUS) -> Eat(MINUS)
        else -> Error()
      }
      val right = Operand()
      left = when {
        op.GetType().equals(PLUS) -> left + right
        op.GetType().equals(MINUS) -> left - right
        else -> Error()
      }
    }
    return left
  }

  //
  // Process operand rule
  //
  // operand : factor ((MUL | DIV) factor) *
  // factor  : INTEGER | LPAR expr RPAR
  //
  private fun Operand(): Int {
    var left = Factor()
    while (currentToken.GetType() == MUL || currentToken.GetType() == DIV) {
      val op = currentToken
      when {
        op.GetType().equals(MUL) -> Eat(MUL)
        op.GetType().equals(DIV) -> Eat(DIV)
        else -> Error()
      }
      val right = Operand()
      left = when {
        op.GetType().equals(MUL) -> left * right
        op.GetType().equals(DIV) -> left / right
        else -> Error()
      }
    }
    return left
  }

  //
  // Process factor rule
  //
  // factor  : INTEGER | LPAR expr RPAR
  //
  private fun Factor(): Int {
    val token = currentToken
    if (token.GetType() == INTEGER) {
      Eat(INTEGER)
      return when(token) {
        is IntegerToken -> token.GetValue()
        else -> Error()
      }
    }
    if (token.GetType() == LPAR) {
      Eat(LPAR)
      val res = Expr()
      Eat(RPAR)
      return res
    }
    Error()
  }

  private fun Eat(tokenType: TokenType) {
    if (currentToken.GetType() == tokenType) {
      currentToken = lexer.GetNextToken()
    }
    else {
      Error()
    }
  }

  private fun Error(): Nothing {
    throw Exception("Syntax error.")
  }
}


fun MakeInterpreter(text: String) = Interpreter(Lexer(text))
