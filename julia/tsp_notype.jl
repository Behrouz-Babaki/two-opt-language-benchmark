using Printf

function read_distances(filename)
    open(filename, "r") do file
        n = parse(Int, readline(file))
        distances = [parse.(Float64, split(readline(file))) for _ in 1:n]
        return distances
    end
end

function two_opt!(tour, distances)
    n = length(tour)
    for i in 1:n-1
        for j in i+2:n
            change = (
                -distances[tour[i]][tour[i+1]]
                -distances[tour[j]][tour[mod1(j+1, n)]]
                +distances[tour[i]][tour[j]]
                +distances[tour[i+1]][tour[mod1(j+1, n)]]
            )
            if change < -1e-10
                reverse!(@view tour[i+1:j])
                return change
            end
        end
    end
    return 0.0
end

function optimize_tour(distances)
    n = length(distances)
    tour = collect(1:n)
    total_improvement = 0.0
    iterations = 0
    max_iterations = 10000

    while iterations < max_iterations
        improvement = two_opt!(tour, distances)
        if improvement >= 0
            break
        end
        total_improvement += improvement
        iterations += 1
    end

    return tour, total_improvement, iterations
end

function main(filename)
    distances = read_distances(filename)
    num_runs = 10
    total_time = 0.0

    for run in 1:num_runs
        start_time = time()
        tour, total_improvement, iterations = optimize_tour(distances)
        end_time = time()
        time_spent = end_time - start_time
        total_time += time_spent

        if run == 1
            println("Optimized tour: ", join(tour, " "))
            @printf("Total improvement: %.6f\n", -total_improvement)
            println("Iterations: ", iterations)
        end
    end

    average_time = total_time / num_runs
    @printf("Average time spent: %.6f seconds\n", average_time)
end

if length(ARGS) < 1
    println(stderr, "Please provide the filename as an argument.")
    exit(1)
end

main(ARGS[1])
