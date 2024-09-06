using Printf

struct OptimizationResult
    tour::Vector{Int}
    total_improvement::Float64
    iterations::Int
end

function read_distances(filename::String)
    open(filename, "r") do file
        n = parse(Int, readline(file))
        distances = Matrix{Float64}(undef, n, n)
        for i in 1:n
            distances[i, :] = parse.(Float64, split(readline(file)))
        end
        return distances
    end
end

function two_opt!(tour::Vector{Int}, distances::Matrix{Float64})
    n = length(tour)
    @inbounds for i in 1:n-1
        for j in i+2:n
            change = -distances[tour[i], tour[i+1]] - distances[tour[j], tour[mod1(j+1, n)]] +
                      distances[tour[i], tour[j]] + distances[tour[i+1], tour[mod1(j+1, n)]]
            
            if change < -1e-10  # Use a small threshold to account for floating-point precision
                # Apply the first improving move
                reverse!(@view tour[i+1:j])
                return change
            end
        end
    end
    return 0.0  # No improvement found
end

function optimize_tour(distances::Matrix{Float64})
    n = size(distances, 1)
    tour = collect(1:n)
    total_improvement = 0.0
    iterations = 0
    MAX_ITERATIONS = 10000

    while iterations < MAX_ITERATIONS
        improvement = two_opt!(tour, distances)
        if improvement >= 0
            break
        end
        total_improvement += improvement
        iterations += 1
    end

    OptimizationResult(tour, total_improvement, iterations)
end

function main(filename::String)
    distances = read_distances(filename)
    n = size(distances, 1)
    num_runs = 10
    total_time = 0.0

    for run in 1:num_runs
        start_time = time()
        result = optimize_tour(distances)
        end_time = time()
        time_spent = end_time - start_time
        total_time += time_spent

        if run == 1
            println("Optimized tour: ", join(result.tour, " "))
            @printf("Total improvement: %f\n", -result.total_improvement)
            println("Iterations: ", result.iterations)
        end
    end

    average_time = total_time / num_runs
    @printf("Average time spent: %f seconds\n", average_time)
end

if length(ARGS) < 1
    println(stderr, "Please provide the filename as an argument.")
    exit(1)
end

main(ARGS[1])
