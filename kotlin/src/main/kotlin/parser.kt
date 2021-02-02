package interpreter

class Parser(private val lexer: Lexer) {
  private var currentToken: Token = lexer.GetNextToken()

  //
  // Parse arithmetic expression.
  //
  // Returns the root of the abstract syntax tree.
  //
  fun Parse() = Expr()

  //
  // Process expr rule
  //
  // expr    : operand ((PLUS | MINUS) operand) *
  // operand : factor ((MUL | DIV) factor) *
  // factor  : INTEGER | LPAR expr RPAR
  //
  private fun Expr(): AstNode {
    var left: AstNode = Operand()

    while (currentToken.GetType() == PLUS || currentToken.GetType() == MINUS) {
      val op = currentToken as OperatorToken
      when {
        op.GetType().equals(PLUS) -> Eat(PLUS)
        op.GetType().equals(MINUS) -> Eat(MINUS)
        else -> Error()
      }
      val right: AstNode = Operand()
      left = BinaryOperationNode(left=left, op=op, right=right)
    }
    return left
  }

  //
  // Process operand rule
  //
  // operand : factor ((MUL | DIV) factor) *
  // factor  : INTEGER | LPAR expr RPAR
  //
  private fun Operand(): AstNode {
    var left = Factor()
    while (currentToken.GetType() == MUL || currentToken.GetType() == DIV) {
      val op = currentToken as OperatorToken
      when {
        op.GetType().equals(MUL) -> Eat(MUL)
        op.GetType().equals(DIV) -> Eat(DIV)
        else -> Error()
      }
      val right = Operand()
      left = BinaryOperationNode(left=left, op=op, right=right)
    }
    return left
  }

  //
  // Process factor rule
  //
  // factor  : INTEGER | LPAR expr RPAR
  //
  private fun Factor(): AstNode {
    val token = currentToken
    if (token.GetType() == INTEGER) {
      Eat(INTEGER)
      return when(token) {
        is IntegerToken -> IntegerNode(token.GetValue())
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
