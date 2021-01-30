package interpreter


import org.junit.Test
import org.junit.Assert.assertEquals


private val THE_ANSWER = 42

private val MIN = 100
private val MAX = 10000


class InterpreterTest {
  @Test
  fun TestNumber() {
    val i = MakeInterpreter("42")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestNumberRnd() {
    val x = (MIN..MAX).random()
    val i = MakeInterpreter("$x")
    assertEquals(x, i.Execute())
  }

  @Test
  fun TestPlus() {
    val i = MakeInterpreter("11 + 31")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestPlusRnd() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val i = MakeInterpreter("$x1 + $x2")
    assertEquals(x1 + x2, i.Execute())
  }

  @Test
  fun TestMinus() {
    val i = MakeInterpreter("111 - 69")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestMinusRnd() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val i = MakeInterpreter("$x1 - $x2")
    assertEquals(x1 - x2, i.Execute())
  }

  @Test
  fun TestMul() {
    val i = MakeInterpreter("6 * 7")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestMulRnd() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val i = MakeInterpreter("$x1 * $x2")
    assertEquals(x1 * x2, i.Execute())
  }

  @Test
  fun TestDiv() {
    val i = MakeInterpreter("294 / 7")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestDivRnd() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val i = MakeInterpreter("$x1 / $x2")
    assertEquals(x1 / x2, i.Execute())
  }

  @Test
  fun TestPlusMinusPlusMinus() {
    val i = MakeInterpreter("12 + 10 - 6 + 56 - 30")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestPlusMinusRnd() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val x3 = (MIN..MAX).random()
    val x4 = (MIN..MAX).random()
    val i = MakeInterpreter("$x1 + $x2 - $x3 + $x4")
    assertEquals(x1 + x2 - x3 + x4, i.Execute())
  }

  @Test
  fun TestComplexExpression0() {
    val i = MakeInterpreter("700 / 7 + 11 * 2 - 16 * 5")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestComplexExpressionRnd0() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val x3 = (MIN..MAX).random()
    val x4 = (MIN..MAX).random()
    val x5 = (MIN..MAX).random()
    val x6 = (MIN..MAX).random()
    val i = MakeInterpreter("$x1 / $x2 + $x3 * $x4 - $x5 * $x6")
    assertEquals(x1 / x2 + x3 * x4 - x5 * x6, i.Execute())
  }

  @Test
  fun TestComplexExpression1() {
    val i = MakeInterpreter("(561 - 5 * (52 + 59)) * (28 - 21)")
    assertEquals(THE_ANSWER, i.Execute())
  }

  @Test
  fun TestComplexExpressionRnd1() {
    val x1 = (MIN..MAX).random()
    val x2 = (MIN..MAX).random()
    val x3 = (MIN..MAX).random()
    val x4 = (MIN..MAX).random()
    val x5 = (MIN..MAX).random()
    val x6 = (MIN..MAX).random()
    val i = MakeInterpreter("(($x1 - $x2) * ($x3 + $x4)) * ($x5 - $x6)")
    assertEquals(((x1 - x2) * (x3 + x4)) * (x5 - x6), i.Execute())
  }

}


private fun MakeInterpreter(text: String) = Interpreter(Lexer(text))
