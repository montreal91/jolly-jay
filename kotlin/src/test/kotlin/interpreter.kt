package interpreter

import org.junit.Test
import org.junit.Assert.assertEquals


val THE_ANSWER = 42


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
  fun TestPlusMinusPlusMinus() {
    val i = MakeInterpreter("12 + 10 - 6 + 56 - 30")
    assertEquals(THE_ANSWER, i.Execute())
  }
}


private fun MakeInterpreter(text: String) = Interpreter(Lexer(text))
