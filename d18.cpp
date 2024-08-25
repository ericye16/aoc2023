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

struct Line
{
    string dir;
    int length;
    string color;
};

Line ParseLine(const string &l)
{
    Line lout;
    // cout << "parsing " << l << "\n";
    CHECK(RE2::FullMatch(l, R"re((\w) (\d+) \(#(\w{6})\))re", &lout.dir, &lout.length, &lout.color));
    return lout;
}

struct Line2
{
    uint64_t length;
    string dir;
};

Line2 Line1toLine2(const Line &line)
{
    string length_s = line.color.substr(0, 5);
    Line2 l2;
    l2.length = stoull(length_s, nullptr, 16);
    int diri = strtol(line.color.substr(5, 1).c_str(), nullptr, 10);
    switch (diri)
    {
    case 0:
        l2.dir = "R";
        break;
    case 1:
        l2.dir = "D";
        break;
    case 2:
        l2.dir = "L";
        break;
    case 3:
        l2.dir = "U";
        break;
    default:
        cerr << "ahhh!!! direction " << diri << endl;
        exit(1);
    }
    return l2;
}

void printLine(const Line &l)
{
    cout << l.dir << " " << l.length << " " << l.color << "\n";
}

string openFile(const string &filename)
{
    ifstream f(filename);
    if (!f.good())
    {
        cerr << "Not good!\n";
        exit(1);
    }
    stringstream ss;
    ss << f.rdbuf();
    cout << ss.str();
    return ss.str();
}

void printTrench(const set<pair<int, int>> &g, int miny, int maxy, int minx, int maxx)
{
    int x, y;
    for (y = miny; y <= maxy; ++y)
    {
        for (x = minx; x <= maxx; ++x)
        {
            if (x == 0 && y == 0)
            {
                cout << "O";
            }
            else if (g.count(make_pair(x, y)) > 0)
            {
                cout << "#";
            }
            else
            {
                cout << ".";
            }
        }
        cout << "\n";
    }
}

int p1(const std::string &input)
{
    set<pair<int, int>> grid;
    string::size_type s = 0;
    string::size_type n = input.find('\n');
    vector<Line> lines;
    while (s != string::npos)
    {
        string line = input.substr(s, n - s);
        if (line.length() < 1)
            break;
        lines.push_back(ParseLine(line));
        if (n == string::npos)
            break;
        s = n + 1;
        n = input.find('\n', s);
    }
    int x = 0, y = 0;
    // x++ = R
    // y++ = U
    int minx = 0, maxx = 0, miny = 0, maxy = 0;
    for (const auto &line : lines)
    {
        printLine(line);
        for (int j = 0; j < line.length; ++j)
        {
            if (line.dir == "R")
                x++;
            else if (line.dir == "L")
                x--;
            else if (line.dir == "U")
                y--;
            else if (line.dir == "D")
                y++;
            else
            {
                cerr << "dir?? " << line.dir << endl;
                exit(-1);
            }
            cout << "inserting " << x << "," << y << endl;
            if (x > maxx)
                maxx = x;
            if (x < minx)
                minx = x;
            if (y > maxy)
                maxy = y;
            if (y < miny)
                miny = y;
            grid.insert(make_pair(x, y));
        }
    }

    printTrench(grid, miny, maxy, minx, maxx);

    int in_x = 0;
    int in_y = 0;
    for (y = miny; y <= maxy; ++y)
    {
        int countx = 0;
        for (x = minx; x <= maxx; ++x)
        {
            if (grid.count(make_pair(x, y)) > 0)
            {
                countx++;
            }
            else
            {
                if (countx == 1)
                {
                    cout << "Found interior box at " << x << " " << y << "\n";
                    in_x = x;
                    in_y = y;
                    goto bout;
                }
                else if (countx > 1)
                {
                    break;
                }
            }
        }
    }
bout:

    vector<pair<int, int>> edges;
    edges.push_back(make_pair(in_x, in_y));
    while (edges.size())
    {
        pair<int, int> p = edges.back();
        edges.pop_back();
        x = p.first;
        y = p.second;
        pair<int, int> p2 = {x + 1, y};
        if (!grid.count(p2))
        {
            edges.push_back(p2);
        }
        p2 = {x - 1, y};
        if (!grid.count(p2))
        {
            edges.push_back(p2);
        }
        p2 = {x, y + 1};
        if (!grid.count(p2))
        {
            edges.push_back(p2);
        }
        p2 = {x, y - 1};
        if (!grid.count(p2))
        {
            edges.push_back(p2);
        }
        grid.insert(p);
    }
    printTrench(grid, miny, maxy, minx, maxx);
    return grid.size();
}

static void push_back_around(set<int64_t> &s, int i)
{
    s.insert(i - 1);
    s.insert(i);
    s.insert(i + 1);
}

uint64_t p2(const std::string &input)
{
    set<pair<int, int>> gridi;
    set<int64_t> xes;
    set<int64_t> yes;
    xes.insert(0);
    yes.insert(0);

    string::size_type s = 0;
    string::size_type n = input.find('\n');
    vector<Line> lines;
    vector<Line2> line2s;
    while (s != string::npos)
    {
        string line = input.substr(s, n - s);
        if (line.length() < 1)
            break;
        Line ll = ParseLine(line);
        lines.push_back(ll);
        line2s.push_back(Line1toLine2(ll));
        if (n == string::npos)
            break;
        s = n + 1;
        n = input.find('\n', s);
    }
    int64_t x = 0, y = 0;
    // x++ = R
    // y++ = D
    int64_t minx = 0, maxx = 0, miny = 0, maxy = 0;
    for (const auto &line : line2s)
    {
        if (line.dir == "R")
            x += line.length;
        else if (line.dir == "L")
            x -= line.length;
        else if (line.dir == "U")
            y -= line.length;
        else if (line.dir == "D")
            y += line.length;
        else
        {
            cerr << "dir?? " << line.dir << endl;
            exit(-1);
        }
        push_back_around(xes, x);
        push_back_around(yes, y);
        if (x > maxx)
            maxx = x;
        if (y > maxy)
            maxy = y;
        if (x < minx)
            minx = x;
        if (y < miny)
            miny = y;
    }
    unordered_map<int64_t, int> x_indices;
    unordered_map<int64_t, int> y_indices;
    int i = 0;
    for (int64_t x : xes)
    {
        x_indices[x] = i;
        i++;
    }
    i = 0;
    for (int64_t y : yes)
    {
        y_indices[y] = i;
        i++;
    }

    cout << "xes size " << xes.size() << " yes size " << yes.size() << endl;
    x = 0, y = 0;
    int xi = x_indices[0];
    int yi = y_indices[0];
    for (const auto &line : line2s)
    {
        cout << "line: " << line.dir << " " << line.length << endl;;
        if (x_indices[x] != xi || y_indices[y] != yi)
        {
            cerr << "xi x or yi y mismatch " << x << " " << y << " " << xi << " " << yi << " " << x_indices[x] << " " << y_indices[y] << endl;
            exit(1);
        }
        cout << "x " << x << "y " << y << " xi " << xi << " yi " << yi << endl;
        if (line.dir == "R")
        {
            x += line.length;
            while (xi < x_indices[x])
            {
                xi++;
                gridi.insert(make_pair(xi, yi));
            }
        }
        else if (line.dir == "L")
        {
            x -= line.length;
            while (xi > x_indices[x])
            {
                xi--;
                gridi.insert(make_pair(xi, yi));
            }
        }
        else if (line.dir == "U")
        {
            y -= line.length;
            while (yi > y_indices[y])
            {
                yi--;
                gridi.insert(make_pair(xi, yi));
            }
        }
        else if (line.dir == "D")
        {
            y += line.length;
            while (yi < y_indices[y])
            {
                yi++;
                gridi.insert(make_pair(xi, yi));
            }
        }
        else
        {
            cerr << "dir?? " << line.dir << endl;
            exit(-1);
        }
    }

    printTrench(gridi, 0, yes.size(), 0, xes.size());
    int in_xi = 0;
    int in_yi = 0;
    for (yi = 0; yi < yes.size(); ++yi)
    {
        int countx = 0;
        for (xi = 0; xi < xes.size(); ++xi)
        {
            if (gridi.count(make_pair(xi, yi)) > 0)
            {
                countx++;
            }
            else
            {
                if (countx == 1)
                {
                    cout << "Found interior box at " << xi << " " << yi << "\n";
                    in_xi = xi;
                    in_yi = yi;
                    goto bout;
                }
                else if (countx > 1)
                {
                    break;
                }
            }
        }
    }
bout:

    vector<pair<int, int>> edges;
    edges.push_back(make_pair(in_xi, in_yi));
    while (edges.size())
    {
        pair<int, int> p = edges.back();
        edges.pop_back();
        x = p.first;
        y = p.second;
        pair<int, int> p2 = {x + 1, y};
        if (!gridi.count(p2))
        {
            edges.push_back(p2);
        }
        p2 = {x - 1, y};
        if (!gridi.count(p2))
        {
            edges.push_back(p2);
        }
        p2 = {x, y + 1};
        if (!gridi.count(p2))
        {
            edges.push_back(p2);
        }
        p2 = {x, y - 1};
        if (!gridi.count(p2))
        {
            edges.push_back(p2);
        }
        gridi.insert(p);
    }
    printTrench(gridi, 0, yes.size(), 0, xes.size());
    vector<int64_t> vxes(xes.begin(), xes.end());
    vector<int64_t> vyes(yes.begin(), yes.end());
    int64_t ss = 0;
    for (auto& p : gridi) {
        xi = p.first;
        yi = p.second;
        assert(xi > 0);
        assert(yi > 0);
        assert(xi < vxes.size());
        assert(yi < vyes.size());
        int64_t g_size = (vxes[xi] - vxes[xi - 1]) * (vyes[yi] - vyes[yi - 1]);
        ss += g_size;
    }
    return ss;
}
int main(int argc, const char *argv[])
{
    string input;
    if (argc > 1)
    {
        input = openFile(argv[1]);
    }
    else
    {
        input = example;
    }
    int gsize = p1(input);
    cout << "1Number in trench: " << gsize << "\n";

    uint64_t gsize2 = p2(input);
    cout << "2Number in trench: " << gsize2 << "\n";

    return 0;
}