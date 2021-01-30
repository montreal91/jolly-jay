package interpreter


typealias TokenType = String
typealias OperatorValueType = String

val INTEGER: TokenType = "INTEGER"
val PLUS: TokenType = "PLUS"
val MINUS: TokenType = "MINUS"
val MUL: TokenType = "MUL"
val DIV: TokenType = "DIV"
val LPAR: TokenType = "LPAR"
val RPAR: TokenType = "RPAR"
val EOF: TokenType = "EOF"

val OPERATORS = listOf('+', '-', '*', '/')


open class Token(private val type_: TokenType) {
  fun GetType(): TokenType {
    return type_
  }
}

class IntegerToken(val type_: TokenType, private val value: Int) : Token(type_) {
  fun GetValue(): Int {
    return value
  }
}

class OperatorToken(
  val type_: TokenType, private val value: OperatorValueType
) : Token(type_) {
  fun GetValue(): OperatorValueType {
    return value;
  }
}

typealias ParenToken = OperatorToken
