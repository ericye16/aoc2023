#include <fstream>
#include <iostream>
#include <string>
#include <set>
#include <sstream>
#include <unordered_set>
#include <utility>

#include "absl/log/check.h"
#include "re2/re2.h"

using namespace std; // fite me

static const string example =
R"(R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3))";

struct Line {
    string dir;
    int length;
    string color;
};

Line ParseLine(const string& l) {
    Line lout;
    // cout << "parsing " << l << "\n";
    CHECK(RE2::FullMatch(l, R"re((\w) (\d+) \(#(\w{6})\))re", &lout.dir, &lout.length, &lout.color));
    return lout;
}

void printLine(const Line& l) {
    cout << l.dir << " " << l.length << " " << l.color << "\n";
}

string openFile(const string &filename) {
    ifstream f(filename);
    if (!f.good()) {
        cerr << "Not good!\n";
        exit(1);
    }
    stringstream ss;
    ss << f.rdbuf();
    cout << ss.str();
    return ss.str();
}


void printTrench(const set<pair<int, int>>& g, int miny, int maxy, int minx, int maxx){
    int x, y; 
    for (y = miny; y <= maxy; ++y) {
        for (x = minx; x <= maxx; ++x) {
            if (x == 0 && y == 0) {
                cout << "O";
            } else if (g.count(make_pair(x, y)) > 0) {
                cout << "#";
            } else  {
                cout << ".";
            }
        }
        cout << "\n";
    }
}

int main(int argc, const char* argv[])
{
    set<pair<int, int>> grid;
    string::size_type s = 0;
    string input;
    if (argc > 1) {
        input = openFile(argv[1]);
    } else {
        input = example;
    }
    cout << "Input: " << input;
    string::size_type n = input.find('\n');
    vector<Line> lines;
    while (s != string::npos) {
        string line = input.substr(s, n - s);
        if (line.length() < 1) break;
        lines.push_back(ParseLine(line));
        if (n == string::npos) break;
        s = n + 1;
        n = input.find('\n', s);
    }
    int x = 0, y = 0;
    // x++ = R
    // y++ = U
    int minx = 0, maxx = 0, miny = 0, maxy = 0;
    for (const auto& line: lines) {
        printLine(line);
        for (int j = 0; j < line.length; ++j) {
            if (line.dir == "R") x++;
            else if (line.dir == "L") x--;
            else if (line.dir == "U") y--;
            else if (line.dir == "D") y++;
            else {
                cerr << "dir?? " << line.dir << endl;
                exit(-1);
            }
            cout << "inserting " << x << "," << y << endl;
            if (x > maxx) maxx = x;
            if (x < minx) minx = x;
            if (y > maxy) maxy = y;
            if (y < miny) miny = y;
            grid.insert(make_pair(x, y));
        }
    }

    printTrench(grid, miny, maxy, minx, maxx);

    int in_x = 0;
    int in_y = 0;
    for (y = miny; y <= maxy; ++y) {
        int countx = 0;
        for (x = minx; x <= maxx; ++x) {
            if (grid.count(make_pair(x, y)) > 0) {
                countx++;
            } else {
                if (countx == 1) {
                    cout << "Found interior box at " << x << " " << y << "\n";
                    in_x = x;
                    in_y = y;
                    goto bout;
                } else if (countx > 1) {
                    break;
                }
            }
        }
    }
    bout:
    
    vector<pair<int, int>> edges;
    edges.push_back(make_pair(in_x, in_y));
    while (edges.size()) {
        pair<int, int> p = edges.back();
        edges.pop_back();
        x = p.first;
        y = p.second;
        pair<int, int> p2 = {x + 1, y};
        if (!grid.count(p2)) {
            edges.push_back(p2);
        }
        p2 = {x - 1, y};
        if (!grid.count(p2)) {
            edges.push_back(p2);
        }
        p2 = {x, y + 1};
        if (!grid.count(p2)) {
            edges.push_back(p2);
        }
        p2 = {x, y - 1};
        if (!grid.count(p2)) {
            edges.push_back(p2);
        }
        grid.insert(p);
    }
    printTrench(grid, miny, maxy, minx, maxx);

    cout << "Number in trench: " << grid.size() << "\n";
    
    return 0;
}