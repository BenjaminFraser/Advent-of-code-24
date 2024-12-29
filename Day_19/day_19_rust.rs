use std::fs;
use std::io::{self, BufRead};
use std::time::Instant;

/// Counts the number of ways the given substrings can be combined (with repetition)
/// to form the target string.
///
/// # Arguments
/// - `substrings`: A vector of substrings that can be used to construct the target.
/// - `target`: The target string to be formed using the substrings.
///
/// # Returns
/// The number of ways the substrings can be combined to form the target string.
fn count_combinations(substrings: &Vec<String>, target: &str) -> usize {
    let n = target.len();
    let mut dp = vec![0; n + 1];
    dp[0] = 1; // Base case: one way to form the empty string

    for i in 1..=n {
        for sub in substrings {
            let sub_len = sub.len();
            if i >= sub_len && &target[i - sub_len..i] == sub {
                dp[i] += dp[i - sub_len];
            }
        }
    }

    dp[n]
}

/// Sums the total solutions for the given designs and patterns.
///
/// # Arguments
/// - `patterns`: A vector of substrings (patterns).
/// - `designs`: A vector of target strings (designs).
///
/// # Returns
/// The sum of the number of ways the patterns can be combined to form all designs.
fn get_results_count_combinations(patterns: Vec<String>, designs: Vec<String>) -> usize {
    let mut total_count = 0;

    for design in designs {
        // Filter relevant substrings for this design
        let relevant_substrings: Vec<String> = patterns
            .iter()
            .cloned()
            .filter(|pattern| design.contains(pattern))
            .collect();

        // Solve for the current design
        total_count += count_combinations(&relevant_substrings, &design);
    }

    total_count
}

fn main() -> io::Result<()> {
    // Read the input file
    // let input_file = "example_input_day_19.txt";
    let input_file = "day_19_input.txt";
    let file = fs::File::open(input_file)?;
    let reader = io::BufReader::new(file);

    let mut lines = reader.lines().filter_map(|line| line.ok());

    // First line contains the patterns
    let patterns: Vec<String> = lines
        .next()
        .unwrap_or_default()
        .split(',')
        .map(|s| s.trim().to_string())
        .collect();

    // Remaining lines are the designs, ignoring any blank lines
    let designs: Vec<String> = lines.filter(|line| !line.trim().is_empty()).collect();

    // Start timing
    let start_time = Instant::now();

    // Calculate and print the result
    let result = get_results_count_combinations(patterns, designs);

    // Measure elapsed time
    let elapsed_time = start_time.elapsed();

    // Print results and timing
    println!("Total combinations: {}", result);
    println!("Execution time: {:.2?}", elapsed_time);

    Ok(())
}