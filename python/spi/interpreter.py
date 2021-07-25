from spi.token import TokenType
from spi.node_visitor import NodeVisitor
from spi.semantic_analyzer import SemanticAnalyzer
from spi.call_stack import CallStack
from spi.activation_record import ActivationRecord
from spi.activation_record import ArType


class Interpreter(NodeVisitor):
    def __init__(self, parser, should_log_stack=False):
        self._parser = parser
        self._call_stack = CallStack()
        self._should_log_stack = should_log_stack

    def execute(self):
        """
        Executes a pascal program.
        """
        tree = self._parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(tree)
        return self._visit(tree)

    def get_current_ar_for_test(self):
        return self._call_stack.peek()

    # TODO: refactor it to make nicer function names
    def _visit_ProcedureDeclaration(self, node):
        ar = self._call_stack.peek()
        ar[node.proc_name] = node

    def _visit_Program(self, node):
        self._log(f"ENTERING: PROGRAM {node.name}")

        ar = ActivationRecord(
            name=node.name,
            ar_type=ArType.PROGRAM,
            nesting_level=1
        )
        self._call_stack.push(ar)

        self._log(str(self._call_stack))

        self._visit(node.block)

        self._log(f"LEAVING: PROGRAM {node.name}")
        self._log(str(self._call_stack))

        self._call_stack.pop()

    def _visit_Block(self, node):
        for decl in node.declarations:
            self._visit(decl)
        self._visit(node.compound_statement)

    def _visit_VarDeclaration(self, node):
        # Do nothing
        pass

    def _visit_Type(self, node):
        # Do nothing
        pass

    def _visit_BinaryOperation(self, node):
        if node.op.get_type() == TokenType.PLUS:
            return self._visit(node.left) + self._visit(node.right)
        elif node.op.get_type() == TokenType.MINUS:
            return self._visit(node.left) - self._visit(node.right)
        elif node.op.get_type() == TokenType.MULTIPLY:
            return self._visit(node.left) * self._visit(node.right)
        elif node.op.get_type() == TokenType.INTEGER_DIV:
            return self._visit(node.left) // self._visit(node.right)
        elif node.op.get_type() == TokenType.REAL_DIV:
            return self._visit(node.left) / self._visit(node.right)
        else:
            self._error()

    def _visit_Number(self, node):
        return node.value

    def _visit_UnaryOperation(self, node):
        val = self._visit(node.right)
        if node.op.get_type() == TokenType.MINUS:
            return -val
        return val

    def _visit_Compound(self, node):
        for child in node.children:
            self._visit(child)

    def _visit_NoOp(self, node):
        pass

    def _visit_Assign(self, node):
        var_name = node.left.value
        var_value = self._visit(node.right)
        ar = self._call_stack.peek()
        ar[var_name] = var_value

    def _visit_Var(self, node):
        var_name = node.value
        ar = self._call_stack.peek()
        return ar.get(var_name)

    def _visit_ProcedureCall(self, node):
        self._log(f"ENTERING: PROCEDURE {node.proc_name}")
        current_ar = self._call_stack.peek()
        procedure = current_ar.get(node.proc_name)

        procedure_ar = ActivationRecord(
            name=node.proc_name,
            ar_type=ArType.PROCEDURE,
            nesting_level=current_ar.nesting_level + 1
        )
        for i in range(len(node.actual_params)):
            param_node = procedure.params[i]
            procedure_ar[param_node.get_identifier()] = self._visit(node.actual_params[i])

        self._call_stack.push(procedure_ar)
        self._log(str(self._call_stack))
        self._visit(procedure.block_node)

        self._log(f"LEAVING: PROCEDURE {node.proc_name}")
        self._log(str(self._call_stack))

        self._call_stack.pop()

    def _error(self):
        raise Exception("Incorrect parse tree.")

    def _log(self, msg):
        if self._should_log_stack:
            print(msg)
