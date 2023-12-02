use std::env;
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string())
    }

    result
}

fn digits(line: &str) -> u32 {
    let mut first = None;
    let mut last = 0;
    for ch in line.chars() {
        if ch.is_numeric() {
            let dig = ch.to_digit(10).unwrap();
            if first.is_none() {
                first = Some(dig);
            }
            last = dig;
        }
    }
    first.unwrap() * 10 + last
}

fn p1(lines: &Vec<String>) -> u32 {
    let mut s = 0;
    for line in lines {
        s += digits(line)
    }
    s
}

fn str_to_digit(str: &str) -> Option<u32> {
    let numeric_dig = str.chars().next().unwrap().to_digit(10);
    if numeric_dig.is_some() {
        return numeric_dig;
    }
    if str.starts_with("one") {
        return Some(1);
    } else if str.starts_with("two") {
        return Some(2);
    } else if str.starts_with("three") {
        return Some(3);
    } else if str.starts_with("four") {
        return Some(4);
    } else if str.starts_with("five") {
        return Some(5);
    } else if str.starts_with("six") {
        return Some(6);
    } else if str.starts_with("seven") {
        return Some(7);
    } else if str.starts_with("eight") {
        return Some(8);
    } else if str.starts_with("nine") {
        return Some(9);
    }
    None
}

fn digits2(line: &str) -> u32 {
    let mut first = None;
    let mut last = 0;
    let num_chrs = line.len();
    for ch_idx in 0..num_chrs {
        let str_slice = &line[ch_idx..];
        if let Some(dig) = str_to_digit(str_slice) {
            if first.is_none() {
                first = Some(dig);
            }
            last = dig;
        }
    }
    first.unwrap() * 10 + last
}

fn p2(lines: &Vec<String>) -> u32 {
    let mut s = 0;
    for line in lines {
        let digs = digits2(line);
        dbg!(digs);
        s += digs; 
    }
    s
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let lines = read_lines(&filename);

    // let v = p1(&lines);
    let v2 = p2(&lines);
    // println!("P1: {}", v);
    println!("P2: {}", v2);
}
