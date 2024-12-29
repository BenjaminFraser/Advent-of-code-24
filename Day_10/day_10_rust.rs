use std::collections::HashMap;
use std::time::Instant;

fn apply_rule(num: i64) -> Vec<i64> {
    if num == 0 {
        return vec![1];
    }

    let s = num.to_string();
    let digits = s.len();

    if digits % 2 == 0 {
        let mid = digits / 2;
        let lhs: i64 = s[..mid].parse().unwrap_or(0);
        let rhs: i64 = s[mid..].parse().unwrap_or(0);
        vec![lhs, rhs]
    } else {
        // Safely multiply with overflow check
        match num.checked_mul(2024) {
            Some(result) => vec![result],
            None => {
                eprintln!("Overflow detected while multiplying {} by 2024", num);
                vec![0] // Return 0 or some fallback value
            }
        }
    }
}

fn rec(
    stones: &[i64],
    blinks_left: usize,
    cache: &mut HashMap<(Vec<i64>, usize), i64>, // Updated to use i64
) -> i64 {
    if blinks_left == 0 {
        return stones.len() as i64;
    }

    // Generate cache key
    let cache_key = (stones.to_vec(), blinks_left);

    if let Some(&cached_result) = cache.get(&cache_key) {
        return cached_result;
    }

    let mut total: i64 = 0; // Explicitly specify the type of `total`
    for &stone in stones {
        let new_stones = apply_rule(stone);
        match total.checked_add(rec(&new_stones, blinks_left - 1, cache)) {
            Some(new_total) => total = new_total,
            None => {
                eprintln!("Overflow detected during recursion.");
                return 0; // Return fallback value if overflow occurs
            }
        }
    }

    cache.insert(cache_key, total);
    total
}

fn main() {
    let input_stones: Vec<i64> = vec![8069, 87014, 98, 809367, 525, 0, 9494914, 5]; // Explicit type
    let blinks_left: usize = 75; // Explicit type

    let mut cache: HashMap<(Vec<i64>, usize), i64> = HashMap::new(); // Explicit type

    let start_time = Instant::now();
    let result = rec(&input_stones, blinks_left, &mut cache);
    let elapsed_time = start_time.elapsed();

    println!("Result: {}", result);
    println!("Execution time: {:.2?}", elapsed_time);
}
