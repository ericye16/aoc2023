#include <string>
#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <istream>
#include <vector>

#include "absl/log/check.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
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
    PrintPart(part);
    while (current_workflow != "A" && current_workflow != "R")
    {
        cout << current_workflow << endl;
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
    cout << ss.str();
    return ss.str();
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
        cout << bin << endl;
    }
    cout << "sum: " << s << endl;

    return 0;
}