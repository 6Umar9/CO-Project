#include <algorithm>
#include <bitset>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::vector;

vector<string>
split(const string &str,
      char delimiter) { // split function returns vector of strings
  vector<string> tokens;
  string::size_type start = 0;
  string::size_type end = str.find(delimiter);

  while (end != string::npos) {
    tokens.push_back(str.substr(start, end - start));
    start = end + 1;
    end = str.find(delimiter, start);
  }

  tokens.push_back(str.substr(start));
  return tokens;
}

string fetchregister(string reg) { // register map function returns "-1" if
                                   // error
  std::map<string, string> registermap = {
      {"zero", "00000"}, {"ra", "00001"}, {"sp", "00010"}, {"gp", "00011"},
      {"tp", "00100"},   {"t0", "00101"}, {"t1", "00110"}, {"t2", "00111"},
      {"s0", "01000"},   {"fp", "01000"}, {"s1", "01001"}, {"a0", "01010"},
      {"a1", "01011"},   {"a2", "01100"}, {"a3", "01101"}, {"a4", "01110"},
      {"a5", "01111"},   {"a6", "10000"}, {"a7", "10001"}, {"s2", "10010"},
      {"s3", "10011"},   {"s4", "10100"}, {"s5", "10101"}, {"s6", "10110"},
      {"s7", "10111"},   {"s8", "11000"}, {"s9", "11001"}, {"s10", "11010"},
      {"s11", "11011"},  {"t3", "11100"}, {"t4", "11101"}, {"t5", "11110"},
      {"t6", "11111"}};

  auto checker = registermap.find(reg);
  if (checker == registermap.end()) {
    return "-1";
  }
  return checker->second;
}

int main() {
  std::ifstream inputFile("input.txt"); // input file

  if (!inputFile.is_open()) { // input file check
    std::cerr << "File not found" << endl;
    return 1;
  }

  string line;
  int lineno = 0;                                 // counter for the line no
  unsigned long long programcounter = 0x00000000; // counter for program counter
  std::map<string, unsigned long long>
      labelmap; // map which takes care of labels
  while (std::getline(inputFile, line)) {

    int usex = 0;
    vector<string> labelsplit = split(line, ':'); // split to check for label
    if (size(labelsplit) > 1) { // checks if label and inputs in programcounter
      labelmap[labelsplit[0]] = programcounter;
      usex = 1;
    }

    // split for getting opcode

    vector<string> instructionsplit = split(labelsplit[usex], ' ');
    string opcode = instructionsplit[0]; // opcode
    // cout << opcode << "|| ";
    vector<string> arguementsplit =
        split(instructionsplit[1], ','); // split for the rest of the arguements
    cout << endl;

    ++lineno;
    programcounter += 0x00000004;
  }
  int x;
  cin >> x;
  string s = std::bitset<12>(x).to_string();
  cout << s << endl;
  cout << fetchregister("e3") << endl;
}
