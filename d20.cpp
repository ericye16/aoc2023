#include <string>
#include <cassert>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <istream>
#include <deque>
#include <vector>

#include "absl/log/check.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "absl/log/log.h"
#include "re2/re2.h"

using namespace std;

string example =
    R"""(broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
)""";

string example2 =
    R"""(broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
)""";

enum Node
{
    Button,
    FlipFlop,
    Conj,
};

enum class PulseType
{
    Low,
    High,
};

string PrintPulse(PulseType pulse)
{
    switch (pulse)
    {
    case PulseType::Low:
        return "low";
    case PulseType::High:
        return "high";
    }
}

typedef unordered_map<string, PulseType> ConjState;

struct Rule
{
    Node type;
    string name;
    vector<string> dests;
    PulseType flip_flop_state;
    ConjState conj_state;
};

Rule ParseRule(absl::string_view sv)
{
    std::pair<absl::string_view, absl::string_view> rule_halves = absl::StrSplit(sv, " -> ");
    auto [orig, dests] = rule_halves;
    Rule rule;
    if (orig == "broadcaster")
    {
        rule.type = Button;
        rule.name = std::string(orig);
    }
    else if (orig[0] == '%')
    {
        rule.type = FlipFlop;
        rule.name = std::string(orig.substr(1));
        rule.flip_flop_state = PulseType::Low;
    }
    else if (orig[0] == '&')
    {
        rule.type = Conj;
        rule.name = std::string(orig.substr(1));
    }
    else
    {
        LOG(FATAL) << "orig ? " << orig;
    }
    vector<absl::string_view> dests_v = absl::StrSplit(dests, ", ");
    for (absl::string_view dest : dests_v)
    {
        rule.dests.push_back(std::string(dest));
    }
    return rule;
}

bool ConjAllHigh(const Rule &rule)
{
    ABSL_ASSERT(rule.type == Conj);
    bool all_high = true;
    for (const auto &[k, v] : rule.conj_state)
    {
        if (v == PulseType::Low)
        {
            all_high = false;
        }
    }
    return all_high;
}

typedef unordered_map<std::string, Rule> Machine;

Machine ParseInput(absl::string_view sv)
{
    Machine machine;
    for (absl::string_view line : absl::StrSplit(sv, '\n'))
    {
        if (!line.size())
            break;
        Rule rule = ParseRule(line);
        machine[rule.name] = rule;
    }
    for (const auto &[name, rule] : machine)
    {
        for (const auto &dest : rule.dests)
        {
            if (machine[dest].type == Conj)
            {
                machine[dest].conj_state[name] = PulseType::Low;
            }
        }
    }
    return machine;
}

struct Pulse
{
    PulseType type;
    string dest;
    string source;
};

struct Pulses
{
    int lows;
    int highs;
};

static PulseType Not(PulseType pulse)
{
    switch (pulse)
    {
    case PulseType::Low:
        return PulseType::High;
    case PulseType::High:
        return PulseType::Low;
    }
}

Pulses PressButton(Machine &machine)
{
    Pulses total_pulses = {};
    std::deque<Pulse> pulses;
    pulses.push_back({.type = PulseType::Low,
                      .dest = "broadcaster",
                      .source = "button"});
    total_pulses.lows++;
    auto send_pulses = [&pulses, &total_pulses](PulseType pulse_type, const Rule &rule)
    {
        for (const auto &dest : rule.dests)
        {
            if (pulse_type == PulseType::Low)
            {
                total_pulses.lows++;
            }
            else
            {
                total_pulses.highs++;
            }
            pulses.push_back({
                .type = pulse_type,
                .dest = dest,
                .source = rule.name,
            });
        }
    };
    while (pulses.size())
    {
        Pulse pulse = pulses.front();
        pulses.pop_front();
        // cout << pulse.source << " " << PrintPulse(pulse.type) << " -> " << pulse.dest << endl;
        Rule &rule = machine[pulse.dest];
        switch (rule.type)
        {
        case Button:
            send_pulses(pulse.type, rule);
            break;
        case FlipFlop:
            if (pulse.type == PulseType::Low)
            {
                rule.flip_flop_state = Not(rule.flip_flop_state);
                send_pulses(rule.flip_flop_state, rule);
            }
            break;
        case Conj:
            rule.conj_state[pulse.source] = pulse.type;
            PulseType to_send;
            if (ConjAllHigh(rule))
            {
                to_send = PulseType::Low;
            }
            else
            {
                to_send = PulseType::High;
            }
            send_pulses(to_send, rule);
            break;
        }
    }
    return total_pulses;
}

Pulses Add(Pulses a, Pulses b)
{
    return (Pulses){
        .lows = a.lows + b.lows,
        .highs = a.highs + b.highs,
    };
}

int p1(Machine &machine)
{
    Pulses pulses = {};
    for (int i = 0; i < 1000; i++)
    {
        pulses = Add(pulses, PressButton(machine));
        // cout << "lows " << pulses.lows << " highs " << pulses.highs << endl;
    }
    return pulses.lows * pulses.highs;
}

bool PressButton2(Machine &machine)
{
    std::deque<Pulse> pulses;
    pulses.push_back({.type = PulseType::Low,
                      .dest = "broadcaster",
                      .source = "button"});
    auto send_pulses = [&pulses](PulseType pulse_type, const Rule &rule)
    {
        for (const auto &dest : rule.dests)
        {
            pulses.push_back({
                .type = pulse_type,
                .dest = dest,
                .source = rule.name,
            });
        }
    };
    // cout << "Button " << endl;
    bool rx_lowed = false;
    while (pulses.size())
    {
        Pulse pulse = pulses.front();
        pulses.pop_front();
        if (pulse.dest == "rx" && pulse.type == PulseType::Low)
        {
            rx_lowed = true;
        }
        // cout << pulse.source << " " << PrintPulse(pulse.type) << " -> " << pulse.dest << endl;
        auto it = machine.find(pulse.dest);
        if (it == machine.end())
            continue;
        Rule &rule = it->second;
        switch (rule.type)
        {
        case Button:
            send_pulses(pulse.type, rule);
            break;
        case FlipFlop:
            if (pulse.type == PulseType::Low)
            {
                rule.flip_flop_state = Not(rule.flip_flop_state);
                send_pulses(rule.flip_flop_state, rule);
            }
            break;
        case Conj:
            rule.conj_state[pulse.source] = pulse.type;
            PulseType to_send;
            if (ConjAllHigh(rule))
            {
                to_send = PulseType::Low;
            }
            else
            {
                to_send = PulseType::High;
            }
            send_pulses(to_send, rule);
            break;
        }
    }
    return rx_lowed;
}

int64_t p2(Machine &machine)
{
    int64_t i = 0;
    while (true)
    {
        i++;
        bool rx = PressButton2(machine);
        if (rx)
            break;
    }
    return i;
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
    Machine machine = ParseInput(input);
    Machine machine2 = ParseInput(example2);

    cout << "p1 " << p1(machine2) << endl;
    cout << "p1 " << p1(machine) << endl;

    Machine machine3 = ParseInput(input);
    cout << "p2 " << p2(machine3) << endl;

    return 0;
}