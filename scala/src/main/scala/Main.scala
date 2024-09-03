import scala.util.{Try, Success, Failure}

object Main extends App {
  if (args.length < 1) {
    println("Please provide the filename as an argument.")
    sys.exit(1)
  }

  val filename = args(0)
  val numRuns = 10

  Try {
    val (distances, n) = TSP.readDistances(filename)
    val totalTime = (1 to numRuns).map { run =>
      val startTime = System.nanoTime()
      val result = TSP.optimizeTour(distances)
      val endTime = System.nanoTime()
      val timeSpent = (endTime - startTime) / 1e9

      if (run == 1) {
        println(s"Optimized tour: ${result.tour.mkString(" ")}")
        println(s"Total improvement: ${-result.totalImprovement}")
        println(s"Iterations: ${result.iterations}")
      }

      timeSpent
    }.sum

    val averageTime = totalTime / numRuns
    println(f"Average time spent: $averageTime%.6f seconds")
  } match {
    case Success(_) => // Do nothing, program completed successfully
    case Failure(exception) => 
      println(s"An error occurred: ${exception.getMessage}")
      sys.exit(1)
  }
}
