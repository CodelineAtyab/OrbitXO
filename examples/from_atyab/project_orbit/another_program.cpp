#include <cstdlib>  // For system()
#include <string>   // For string manipulation
#include <iostream> // For output

int main() {
  // Hardcoded input values
  int inp1 = 10;
  int inp2 = 20;
  
  // Construct the command string
  std::string command = "python non_interactive_calc.py " + std::to_string(inp1) + " " + std::to_string(inp2);
  
  // Print the command (optional)
  std::cout << "Executing: " << command << std::endl;
  
  // Make the system call
  system(command.c_str());
  
  return 0;
}