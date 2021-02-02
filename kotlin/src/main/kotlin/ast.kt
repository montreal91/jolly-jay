package interpreter


abstract class AstNode


class IntegerNode(private val value: Int) : AstNode() {
  fun GetValue() = value
}


class BinaryOperationNode(
    private val left: AstNode,
    private val op: OperatorToken,
    private val right: AstNode
) : AstNode() {
  fun GetLeft() = left
  fun GetRight() = right
  fun GetOp() = op
}
