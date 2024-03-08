#include <bitset>
#include <iostream>
#include <map>
#include <string>

using std::cin;
using std::cout;
using std::endl;
using std::string;

string fetchregister(string reg) {
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
  string ret = registermap[reg];
  // if (ret==std::none) {
  //   return "-1";
  // }
  return ret;
}

int main() {
  int x;
  cin >> x;
  string s = std::bitset<12>(x).to_string();
  cout << s << endl;
  cout << fetchregister("e3") << endl;
}
