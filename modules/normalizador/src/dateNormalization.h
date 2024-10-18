#ifndef DATENORMALIZATION_H
#define DATENORMALIZATION_H

#include <iostream>
#include <string>
#include <regex>
#include <sstream>
#include <curl/curl.h>

using namespace std;


string normalizeDate(const string &text, const string &lang = "en");

#endif