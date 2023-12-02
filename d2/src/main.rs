use ascii::AsciiChar;
use ascii::AsciiStr;
use ascii::AsciiString;
use ascii::ToAsciiChar;
use regex::bytes::Regex;
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

#[derive(Debug, Default, Clone, Copy)]
struct Grab {
    red: u32,
    green: u32,
    blue: u32,
}

#[derive(Debug, Default, Clone)]
struct Game {
    id: u32,
    grabs: Vec<Grab>,
}

fn parse_ascii<'a, A, B>(s: A) -> B
where
    A: Into<&'a [u8]> + std::fmt::Debug,
    B: FromStr,
    <B as FromStr>::Err: Debug,
{
    std::str::from_utf8(s.into()).unwrap().parse::<B>().unwrap()
}

fn parse_lines(lines: &Vec<AsciiString>) -> Vec<Game> {
    let mut v = vec![];
    let game_regex = Regex::new(r"Game (\d+)").unwrap();

    for line in lines {
        let game_split = line
            .split(':'.to_ascii_char().unwrap())
            .collect::<Vec<&AsciiStr>>();
        let game_id: u32 = parse_ascii(&game_regex.captures(game_split[0].into()).unwrap()[1]);

        let picked_cubes_str = game_split[1].split(AsciiChar::Semicolon);
        let mut grabs = vec![];
        for picked_cubes in picked_cubes_str {
            let mut grab = Grab::default();
            let cubes_split = picked_cubes
                .split(AsciiChar::Comma)
                .collect::<Vec<&AsciiStr>>();
            for cube in cubes_split {
                let trimmed_cube = cube.trim();
                let number_color: Vec<&AsciiStr> = trimmed_cube.split(AsciiChar::Space).collect();
                let number: u32 = parse_ascii(number_color[0]);
                let color = number_color[1];
                match color.as_str() {
                    "blue" => grab.blue = number,
                    "red" => grab.red = number,
                    "green" => grab.green = number,
                    _ => panic!("{color} not a color!"),
                }
            }
            grabs.push(grab);
        }
        v.push(Game { id: game_id, grabs });
    }
    v
}

fn p1(lines: &Vec<AsciiString>) -> u32 {
    let mut s = 0;
    let games = parse_lines(lines);
    for game in games {
        let mut possible = true;
        for grab in game.grabs {
            if grab.red > 12 || grab.green > 13 || grab.blue > 14 {
                possible = false;
            }
        }
        if possible {
            s += game.id;
        }
    }
    s
}

fn p2(lines: &Vec<AsciiString>) -> u32 {
    let mut s = 0;
    let games = parse_lines(lines);
    for game in games {
        let mut min_grabs = Grab::default();
        for grab in game.grabs {
            if grab.blue > min_grabs.blue {
                min_grabs.blue = grab.blue;
            }
            if grab.green > min_grabs.green {
                min_grabs.green = grab.green;
            }
            if grab.red > min_grabs.red {
                min_grabs.red = grab.red;
            }
        }
        s += min_grabs.blue * min_grabs.green * min_grabs.red;
    }
    s
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let lines = read_lines(&filename);

    let v = p1(&lines);
    let v2 = p2(&lines);
    println!("P1: {}", v);
    println!("P2: {}", v2);
}
