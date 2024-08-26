#include <string>
#include <cassert>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <istream>
#include <vector>

#include "absl/log/check.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "absl/log/log.h"
#include "re2/re2.h"

using namespace std;

string example =
    R"""(px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
)""";

struct Part
{
    int x;
    int m;
    int a;
    int s;
};

Part ParsePart(absl::string_view st)
{
    Part part;
    CHECK(RE2::FullMatch(st, R"re({x=(\d+),m=(\d+),a=(\d+),s=(\d+)})re", &part.x, &part.m, &part.a, &part.s));
    return part;
}

vector<Part> ParseParts(string s)
{
    vector<Part> parts;
    vector<absl::string_view> vs = absl::StrSplit(s, '\n');
    for (absl::string_view part_s : vs)
    {
        if (part_s.length() > 1)
        {

            parts.push_back(ParsePart(part_s));
        }
    }
    return parts;
}

enum class Operation
{
    Gt,
    Lt,
    Always,
};

struct Rule
{
    Operation op;
    int val;
    string quality;
    string target;
};

void PrintRule(const Rule &rule)
{
    if (rule.op == Operation::Always)
    {
        cout << rule.target;
    }
    else
    {
        string op;
        if (rule.op == Operation::Gt)
        {
            op = ">";
        }
        else if (rule.op == Operation::Lt)
        {
            op = "<";
        }
        cout << rule.quality << op << rule.val << ":" << rule.target;
    }
    cout << endl;
}

struct Workflow
{
    string name;
    vector<Rule> rules;
};

Rule ParseRule(absl::string_view s)
{
    Rule rule;
    if (absl::StrContains(s, ':'))
    {
        string op;
        CHECK(RE2::FullMatch(s, R"re((\w)(>|<)(\d+):(\w+))re", &rule.quality, &op, &rule.val, &rule.target));
        if (op == ">")
        {
            rule.op = Operation::Gt;
        }
        else if (op == "<")
        {
            rule.op = Operation::Lt;
        }
        else
        {
            cerr << "op ?? " << op << endl;
            assert(false);
        }
    }
    else
    {
        rule.op = Operation::Always;
        rule.val = 0;
        rule.target = string(s);
    }
    return rule;
}

Workflow ParseWorkflow(string_view s)
{
    Workflow workflow;
    string rules;
    CHECK(RE2::FullMatch(s, R"re((\w+){(.+)})re", &workflow.name, &rules));
    vector<absl::string_view> rules_v = absl::StrSplit(rules, ",");
    for (absl::string_view rules_sv : rules_v)
    {
        workflow.rules.push_back(ParseRule(rules_sv));
    }
    return workflow;
}

typedef unordered_map<string, Workflow> Workflows;

Workflows ParseWorkflows(string_view s)
{
    vector<string_view> s_v = absl::StrSplit(s, '\n');
    Workflows workflows;
    for (string_view ss : s_v)
    {
        Workflow workflow = ParseWorkflow(ss);
        workflows[workflow.name] = workflow;
    }
    return workflows;
}

void PrintPart(const Part &part)
{
    cout << "Part{x=" << part.x << ",m=" << part.m << ",a=" << part.a << ",s=" << part.s << "}" << endl;
}

bool CheckCondition(const Rule &rule, const Part &part)
{
    if (rule.op == Operation::Always)
        return true;
    else
    {
        int val;
        if (rule.quality == "x")
        {
            val = part.x;
        }
        else if (rule.quality == "m")
        {
            val = part.m;
        }
        else if (rule.quality == "a")
        {
            val = part.a;
        }
        else if (rule.quality == "s")
        {
            val = part.s;
        }
        else
        {
            cerr << "quality " << rule.quality << endl;
            ABSL_ASSERT(false);
        }
        if (rule.op == Operation::Gt)
        {
            return val > rule.val;
        }
        else if (rule.op == Operation::Lt)
        {
            return val < rule.val;
        }
        else
        {
            ABSL_ASSERT(false);
        }
    }
}

string ProcessPart(const Workflows &workflows, const Part &part)
{
    string current_workflow = "in";
    // PrintPart(part);
    while (current_workflow != "A" && current_workflow != "R")
    {
        // cout << current_workflow << endl;
        const Workflow &workflow = workflows.at(current_workflow);
        for (const Rule &rule : workflow.rules)
        {
            // PrintRule(rule);
            if (CheckCondition(rule, part))
            {
                current_workflow = rule.target;
                break;
            }
        }
    }
    return current_workflow;
};

int SumPart(const Part &part)
{
    return part.x + part.m + part.a + part.s;
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
    return ss.str();
}

// both sides inclusive
struct Range
{
    int low;
    int high;
};

optional<Range> CombineRanges(const Range &r1, const Range &r2)
{
    Range lowr;
    Range highr;
    if (r1.low < r2.low)
    {
        lowr = r1;
        highr = r2;
    }
    else
    {
        lowr = r2;
        highr = r1;
    }
    if (highr.low > lowr.high)
    {
        // Disjoint, empty set
        return nullopt;
    }
    else
    {
        int high = min(highr.high, lowr.high);
        int low = max(highr.low, lowr.low);
        ABSL_ASSERT(high >= low);
        return Range{.low = low, .high = high};
    }
}

typedef vector<Range> Ranges;

// Pre and post conditions: vrange is sorted, disjoint Ranges
Ranges UnionRanges(const Ranges &vrange, const Range &r)
{
    Ranges out;
    optional<Range> r2 = r;
    for (int i = 0; i < vrange.size(); ++i)
    {
        if (!r2)
        {
            out.push_back(vrange[i]);
        }
        else if (vrange[i].high < r2->low)
        {
            // Disjoint case
            out.push_back(vrange[i]);
        }
        else if (vrange[i].low > r2->high)
        {
            // Disjoint case
            if (r2)
            {
                out.push_back(*r2);
                r2 = nullopt;
            }
            out.push_back(vrange[i]);
        }
        else
        {
            r2->low = min(r2->low, vrange[i].low);
            r2->high = max(r2->high, vrange[i].high);
        }
    }
    if (r2)
    {
        out.push_back(*r2);
        r2 = nullopt;
    }
    return out;
}

std::string PrintRange(const Range &r)
{
    stringstream ss;
    ss << "<" << r.low << "," << r.high << ">";
    return ss.str();
}

struct Partss
{
    Range x;
    Range m;
    Range a;
    Range s;
};

void PrintPartss(const Partss &p)
{
    cout << "x" << PrintRange(p.x) << endl;
    cout << "m" << PrintRange(p.m) << endl;
    cout << "a" << PrintRange(p.a) << endl;
    cout << "s" << PrintRange(p.s) << endl;
}

Partss DefaultParts()
{
    return {
        .x = Range{1, 4000},
        .m = Range{1, 4000},
        .a = Range{1, 4000},
        .s = Range{1, 4000},
    };
}

optional<Partss> CombineParts(const Partss &p1, const Partss &p2)
{
    Partss o;
    auto xo = CombineRanges(p1.x, p2.x);
    if (!xo)
    {
        return nullopt;
    }
    o.x = *xo;

    auto mo = CombineRanges(p1.m, p2.m);
    if (!mo)
    {
        return nullopt;
    }
    o.m = *mo;

    auto ao = CombineRanges(p1.a, p2.a);
    if (!ao)
    {
        return nullopt;
    }
    o.a = *ao;

    auto so = CombineRanges(p1.s, p2.s);
    if (!so)
    {
        return nullopt;
    }
    o.s = *so;
    return o;
}

int64_t CountRanges(const Ranges &rs)
{
    int64_t s = 0;
    int last_high = -1;
    for (const auto &r : rs)
    {
        ABSL_ASSERT(r.high >= r.low);
        ABSL_ASSERT(r.low > last_high);
        last_high = r.high;
        s += r.high - r.low + 1;
    }
    return s;
}

int64_t PartVolume(const Partss &p)
{
    return (int64_t)(p.x.high - p.x.low + 1) *
           (int64_t)(p.m.high - p.m.low + 1) *
           (int64_t)(p.a.high - p.a.low + 1) *
           (int64_t)(p.s.high - p.s.low + 1);
}

int64_t CountParts(const vector<Partss> &parts)
{
    // Inclusion-exclusion time
    int64_t sum = 0;
    vector<pair<Partss, int>> intersections;
    for (const auto &part : parts)
    {
        // PrintPartss(part);
        int intersections_size = intersections.size();
        for (int i = 0; i < intersections_size; ++i)
        {
            if (auto ints = CombineParts(part, intersections[i].first))
            {
                sum += PartVolume(*ints) * intersections[i].second * -1;
                intersections.push_back(make_pair(*ints, intersections[i].second * -1));
            }
        }
        sum += PartVolume(part);
        intersections.push_back(make_pair(part, 1));
    }
    return sum;
}

struct State
{
    string workflow;
    Partss partss;
    int ruleno;
};

int64_t p2(const Workflows &workflows)
{
    vector<State> states;
    states.push_back({
        .workflow = "in",
        .partss = DefaultParts(),
        .ruleno = 0,
    });
    vector<Partss> accepted_parts;
    while (states.size())
    {
        State state = states.back();
        states.pop_back();
        if (state.workflow == "A")
        {
            accepted_parts.push_back(state.partss);
            continue;
        }
        else if (state.workflow == "R")
        {
            continue;
        }
        const Workflow &workflow = workflows.at(state.workflow);
        const Rule &rule = workflow.rules[state.ruleno];
        if (rule.op == Operation::Always)
        {
            if (rule.target == "A")
            {
                accepted_parts.push_back(state.partss);
                continue;
            }
            else if (rule.target == "R")
            {
                // Rejected, drop it
                continue;
            }
            else
            {
                state.workflow = rule.target;
                state.ruleno = 0;
                states.push_back(state);
            }
        }
        else
        {
            Range bisection_winner, bisection_loser;
            if (rule.op == Operation::Gt)
            {
                bisection_winner = Range{rule.val + 1, 4000};
                bisection_loser = Range{1, rule.val};
            }
            else
            {
                bisection_winner = Range{1, rule.val - 1};
                bisection_loser = Range{rule.val, 4000};
            }
            Partss next_winner = DefaultParts();
            Partss next_loser = DefaultParts();
            if (rule.quality == "x")
            {
                next_winner.x = bisection_winner;
                next_loser.x = bisection_loser;
            }
            else if (rule.quality == "m")
            {
                next_winner.m = bisection_winner;
                next_loser.m = bisection_loser;
            }
            else if (rule.quality == "a")
            {
                next_winner.a = bisection_winner;
                next_loser.a = bisection_loser;
            }
            else if (rule.quality == "s")
            {
                next_winner.s = bisection_winner;
                next_loser.s = bisection_loser;
            }
            else
            {
                LOG(FATAL) << "rule quality " << rule.quality << endl;
            }
            optional<Partss> next_winner_o = CombineParts(next_winner, state.partss);
            if (next_winner_o)
            {
                states.push_back(State{
                    .workflow = rule.target,
                    .partss = *next_winner_o,
                    .ruleno = 0,
                });
            }
            optional<Partss> next_lower_o = CombineParts(next_loser, state.partss);
            if (next_lower_o)
            {
                states.push_back(State{
                    .workflow = workflow.name,
                    .partss = *next_lower_o,
                    .ruleno = state.ruleno + 1,
                });
            }
        }
    }
    return CountParts(accepted_parts);
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
    int flow_part_split = input.find("\n\n");
    assert(flow_part_split != string::npos);
    string rules = input.substr(0, flow_part_split);
    string parts_s = input.substr(flow_part_split + 2, string::npos);
    Workflows workflows = ParseWorkflows(rules);
    vector<Part> parts = ParseParts(parts_s);

    int s = 0;
    for (const Part &part : parts)
    {
        string bin = ProcessPart(workflows, part);
        if (bin == "A")
        {
            s += SumPart(part);
        }
        // cout << bin << endl;
    }
    cout << "sum: " << s << endl;

    int64_t ps = p2(workflows);
    cout << "p2: " << ps << endl;

    return 0;
}