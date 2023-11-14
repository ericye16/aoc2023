use std::env;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string())
    }

    result
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let lines = read_lines(&filename);
    let mut max = 0;
    let mut elf = 0;
    for line in &lines {
        if line == "" {
            if elf > max {
                max = elf;
            }
            elf = 0;
        } else {
            let calories: i32 = line.parse().unwrap();
            elf += calories;
        }
    }
    if elf > max {
        max = elf;
    }
    println!("P1: {}", max);
}
