package interpreter

import org.junit.Test
import org.junit.Assert.assertEquals


private val THE_ANSWER = 42


class InterpreterTest {
  @Test
  fun TestNumber() {
    val i = MakeInterpreter("42")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestPlus() {
    val i = MakeInterpreter("11 + 31")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestMinus() {
    val i = MakeInterpreter("111 - 69")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestMul() {
    val i = MakeInterpreter("6 * 7")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestDiv() {
    val i = MakeInterpreter("294 / 7")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestPlusMinusPlusMinus() {
    val i = MakeInterpreter("12 + 10 - 6 + 56 - 30")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestComplexExpression0() {
    val i = MakeInterpreter("700 / 7 + 11 * 2 - 16 * 5")
    assertEquals(THE_ANSWER, i.Execute())
  }
}


private fun MakeInterpreter(text: String) = Interpreter(Lexer(text))
