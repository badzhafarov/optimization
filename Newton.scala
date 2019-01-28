
object Newton extends App{

  val eps = 0.00001

  def f(x: Double): Double = 10*math.pow(x, 5)+9*math.pow(x, 3)-3*math.pow(x, 2)+3

  def dx(x: Double): Double = 50*math.pow(x, 4)+27*math.pow(x, 2)-6*x

  def isGood(x: Double, x_prev: Double): Boolean ={
    if (math.abs(x_prev-x)<eps) true
    else false
  }

  def newtonMethod(f: Double => Double, dx: Double => Double, x: Double): Double = {
    val x_next = x-f(x)/dx(x)
    if (isGood(x_next, x)) x_next
    else newtonMethod(f, dx, x_next)
  }

  def helperSecant(x: Double, x_prev: Double, f: Double => Double): Double = (f(x)-f(x_prev))/(x-x_prev)

  def secantMethod(f: Double => Double, x: Double, x_prev: Double): Double = newtonMethod(f, helperSecant(_, x_prev, f), x)

  println(newtonMethod(f, dx, 0.5))
  println(secantMethod(f, -1, 1))

}
