use std::cmp::Reverse;
use std::env;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string())
    }

    result
}

fn p1(lines: &Vec<String>) -> i32 {
    let mut max = 0;
    let mut elf = 0;
    for line in lines {
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
    max
}

fn p2(lines: &Vec<String>) -> i32 {
    let mut v = vec![];
    let mut elf = 0;
    for line in lines {
        if line == "" {
            v.push(elf);
            elf = 0;
        } else {
            let calories: i32 = line.parse().unwrap();
            elf += calories;
        }
    }
    if elf != 0 {
        v.push(elf);
    }
    v.sort_by_key(|w| Reverse(*w));
    v.iter().take(3).sum()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let lines = read_lines(&filename);

    let max = p1(&lines);
    let max2 = p2(&lines);
    println!("P1: {}", max);
    println!("P2: {}", max2);
}
