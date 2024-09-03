import scala.io.Source
import scala.util.Using

case class OptimizationResult(tour: Array[Int], totalImprovement: Double, iterations: Int)

object TSP {
  def readDistances(filename: String): (Array[Array[Double]], Int) = {
    val lines = Using(Source.fromFile(filename))(_.getLines().toArray).get
    val n = lines.head.toInt
    val distances = lines.tail.map(_.split("\\s+").map(_.toDouble))
    (distances, n)
  }

  def twoOpt(tour: Array[Int], distances: Array[Array[Double]]): Double = {
    val n = tour.length
    for {
      i <- 0 until n - 1
      j <- i + 2 until n
    } {
      val change = -distances(tour(i))(tour(i + 1)) - distances(tour(j))(tour((j + 1) % n)) +
        distances(tour(i))(tour(j)) + distances(tour(i + 1))(tour((j + 1) % n))

      if (change < -1e-10) {
        tour.slice(i + 1, j + 1).reverse.copyToArray(tour, i + 1)
        return change
      }
    }
    0.0
  }

  def optimizeTour(distances: Array[Array[Double]]): OptimizationResult = {
    val n = distances.length
    val tour = Array.range(0, n)
    var totalImprovement = 0.0
    var iterations = 0
    val maxIterations = 10000

    while (iterations < maxIterations) {
      val improvement = twoOpt(tour, distances)
      if (improvement >= 0) {
        return OptimizationResult(tour, totalImprovement, iterations)
      }
      totalImprovement += improvement
      iterations += 1
    }

    OptimizationResult(tour, totalImprovement, iterations)
  }
}
