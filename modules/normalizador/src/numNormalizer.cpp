#include <iostream>
#include <string>
#include <cctype>
#include <unordered_map>
#include <sstream>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <array>
#include <regex>

using namespace std;

// Helper function to run a system command and capture the output
string execCommand(const char* cmd) {
    array<char, 128> buffer;
    string result;
    shared_ptr<FILE> pipe(popen(cmd, "r"), pclose);
    if (!pipe) throw runtime_error("popen() failed!");
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

// Placeholder for numberToWords function 
string numberToWords(const string &number_str, bool ordinal, const string &language) {
    stringstream ss;
    ss << "python3 convert_numbers.py " << number_str << " " 
       << (ordinal ? "True" : "False") << " " << language;
    string result = execCommand(ss.str().c_str());

    if (!result.empty() && result[result.size() - 1] == '\n') {
        result.pop_back();
    }

    return result;
}

// Function to normalize numbers in text
string normalizeNumbers(const string &text, const bool &ordinal = true, const string &language = "en") {
    regex num_regex(R"(\d+)");
    smatch match;
    string result = text;

    // Iterate through the string and find each number match
    size_t search_start = 0;
    while (search_start < result.size()) {
        string current_substring = result.substr(search_start);  
            if (regex_search(current_substring, match, num_regex)) {
            string num_str = match.str();  
            string word_form = numberToWords(num_str, ordinal, language); 

            result.replace(search_start + match.position(0), match.length(0), word_form);
            search_start += match.position(0) + word_form.length();
        } else {
            break;
        }
    }

    return result;
}

//int main() {
//    string texto1 = "1";
//    string texto2 = "123";
//    string te= "5555";
//
//    cout << numberToWords(texto1, false, "pt") << endl;
//    cout << numberToWords(texto2, false, "pt") << endl;
//    cout << numberToWords(te, false, "es") << endl;
//    return 0;
//}//