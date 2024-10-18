#ifndef NUMNORMALIZATION_H
#define NUMNORMALIZATION_H


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

string normalizeNumbers(const string &text, const bool &ordinal = true, const string &language = "en");

#endif