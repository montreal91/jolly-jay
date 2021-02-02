package interpreter

import kotlin.collections.HashMap
import kotlin.collections.hashMapOf


abstract class BaseVisitor {
  protected fun Visit(node: AstNode) = when(node) {
    is IntegerNode -> VisitIntegerNode(node)
    is BinaryOperationNode -> VisitBinaryOperationNode(node)
    else -> Error()
  }

  abstract protected fun VisitIntegerNode(node: IntegerNode): Int
  abstract protected fun VisitBinaryOperationNode(node: BinaryOperationNode): Int
  abstract protected fun Error(): Nothing
}


class Interpreter(private val parser: Parser) : BaseVisitor() {

  //
  // Execute arithmetic expression
  //
  // IN : (561 - 5 * (52 + 59)) * (28 - 21)
  // OUT: 42
  //
  public fun Execute(): Int {
    val tree = parser.Parse()
    return Visit(tree)
  }

  override protected fun VisitBinaryOperationNode(node: BinaryOperationNode): Int {
    val left = Visit(node.GetLeft())
    val right = Visit(node.GetRight())
    val op = node.GetOp().GetType()

    return when {
      op == PLUS -> left + right
      op == MINUS -> left - right
      op == MUL -> left * right
      op == DIV -> left / right
      else -> Error()
    }
  }

  override protected fun VisitIntegerNode(node: IntegerNode) = node.GetValue()

  override protected fun Error(): Nothing {
    throw Exception("Traverse parse tree error.")
  }
}


fun MakeInterpreter(text: String) = Interpreter(Parser(Lexer(text)))
