use ascii::AsciiChar;
use ascii::AsciiString;
use std::env;
use std::fmt::Debug;
use std::fs::read_to_string;
use std::str::FromStr;

fn read_lines(filename: &str) -> Vec<AsciiString> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(AsciiString::from_ascii(line.to_string()).unwrap())
    }

    result
}

fn parse_ascii<'a, A, B>(s: A) -> B
where
    A: Into<&'a [u8]> + std::fmt::Debug,
    B: FromStr,
    <B as FromStr>::Err: Debug,
{
    std::str::from_utf8(s.into()).unwrap().parse::<B>().unwrap()
}

fn p1(lines: &Vec<AsciiString>) -> u32 {
    let mut s = 0;
    for (line_idx, line) in lines.iter().enumerate() {
        let mut col_idx: usize = 0;
        while col_idx < line.len() {
            if line[col_idx].is_ascii_digit() {
                let mut end_of_digit = col_idx + 1;
                while end_of_digit < line.len() && line[end_of_digit].is_ascii_digit() {
                    end_of_digit += 1;
                }
                let part_number: u32 = parse_ascii(&line[col_idx..end_of_digit]);
                let mut is_beside_symbol = false;
                let start_line: i32 = line_idx as i32 - 1;
                let end_line: i32 = line_idx as i32 + 1;
                let start_col: i32 = col_idx as i32 - 1;
                let end_col: i32 = end_of_digit as i32;
                'outer: for query_line in start_line..=end_line {
                    for query_col in start_col..=end_col {
                        if query_line < 0
                            || query_line >= lines.len() as i32
                            || query_col < 0
                            || query_col >= line.len() as i32
                        {
                            continue;
                        }
                        let query_char: AsciiChar =
                            lines[query_line as usize].as_slice()[query_col as usize];
                        if !query_char.is_ascii_digit() && query_char != AsciiChar::Dot {
                            is_beside_symbol = true;
                            break 'outer;
                        }
                    }
                }
                if is_beside_symbol {
                    s += part_number;
                }
                col_idx = end_of_digit;
            } else {
                col_idx += 1;
            }
        }
    }
    s
}

fn find_adjacent_part_numbers(
    lines: &Vec<AsciiString>,
    line_idx: usize,
    col_idx: usize,
) -> Vec<u32> {
    let start_line: i32 = std::cmp::max(line_idx as i32 - 1, 0);
    let end_line: i32 = std::cmp::min(line_idx as i32 + 1, lines.len() as i32 - 1);
    let start_col: i32 = std::cmp::max(col_idx as i32 - 1, 0);
    let end_col: i32 = std::cmp::min(col_idx as i32 + 1, lines[line_idx].len() as i32 - 1);
    let mut v = vec![];
    for query_line in start_line..=end_line {
        let mut query_col = start_col;
        let line = &lines[query_line as usize];
        while query_col <= end_col {
            let query_char = line.as_slice()[query_col as usize];
            if query_char.is_ascii_digit() {
                // search left to find first digit
                let mut before_digit = query_col - 1;
                while before_digit >= 0 && line.as_slice()[before_digit as usize].is_ascii_digit() {
                    before_digit -= 1;
                }
                // search right to find last digit
                let mut after_digit = query_col;
                while after_digit < line.len() as i32
                    && line.as_slice()[after_digit as usize].is_ascii_digit()
                {
                    after_digit += 1;
                }
                v.push(parse_ascii(
                    &line.as_bytes()[(before_digit + 1) as usize..after_digit as usize],
                ));
                query_col = after_digit;
            } else {
                query_col += 1;
            }
        }
    }
    v
}

fn p2(lines: &Vec<AsciiString>) -> u32 {
    let mut s = 0;
    for (line_idx, line) in lines.iter().enumerate() {
        for col_idx in 0..line.len() {
            if line[col_idx] == AsciiChar::Asterisk {
                let adjacent_numbers = find_adjacent_part_numbers(lines, line_idx, col_idx);
                if adjacent_numbers.len() == 2 {
                    s += adjacent_numbers[0] * adjacent_numbers[1];
                }
            }
        }
    }
    s
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let lines = read_lines(&filename);

    println!("P1: {}", p1(&lines));
    println!("P2: {}", p2(&lines));
}
