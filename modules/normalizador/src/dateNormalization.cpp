#include <iostream>
#include <string>
#include <regex>
#include <sstream>
#include <curl/curl.h>

using namespace std;

// Function to write the response data from the API call
size_t WriteCallback(void* contents, size_t size, size_t nmemb, string* userp) {
    size_t totalSize = size * nmemb;
    userp->append((char*)contents, totalSize);
    return totalSize;
}

// Function to get the month name from the API
string getMonthNameFromAPI(const string& lang, int monthNum) {
    CURL* curl;
    CURLcode res;
    string readBuffer;
    
    // Construct the API URL
    string url = "http://localhost:8080/months?lang=" + lang + "&month=" + to_string(monthNum);
    
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    
    curl_global_cleanup();
    
    // Parse the JSON response to extract the month name
    size_t pos = readBuffer.find("month");
    if (pos != string::npos) {
        pos = readBuffer.find("\"", pos + 7);
        size_t endPos = readBuffer.find("\"", pos + 1);
        return readBuffer.substr(pos + 1, endPos - pos - 1);
    }
    
    return "Unknown Month";
}

string normalizeDate(const string &text, const string &lang = "en") {
    string date = text;  
    smatch matches;

    date.erase(remove_if(date.begin(), date.end(), ::isspace), date.end());

    // Check for extended date formats first (e.g., "January 1, 2020")
    //regex extendedRegex(R"((\w+)\s+(\d{1,2}),?\s+(\d{4}))");
    //if (regex_search(date, matches, extendedRegex)) {
    //    string month = matches[1].str(); // Keep month name
    //    int day = stoi(matches[2].str());
    //    int year = stoi(matches[3].str());
    //    return to_string(day) + " " + month + " " + to_string(year);
    //}

    // Check for yyyy-mm-dd format
    regex yyyy_mm_dd_regex(R"((\d{4})[.\-\/\s]+(\d{1,2})[.\-\/\s]+(\d{1,2}))");

    if (regex_search(date, matches, yyyy_mm_dd_regex)) {
        int monthNum = stoi(matches[2].str());
        int day = stoi(matches[3].str());
        int year = stoi(matches[1].str());
        string monthName = getMonthNameFromAPI(lang, monthNum);
        return to_string(day) + " " + monthName + " " + to_string(year);
    }

    // Check for dd-mm-yyyy format
    regex dd_mm_yyyy_regex(R"((\d{1,2})[.\-\/\s]+(\d{1,2})[.\-\/\s]+(\d{4}))");
    if (regex_search(date, matches, dd_mm_yyyy_regex)) {
        int day = stoi(matches[1].str());
        int monthNum = stoi(matches[2].str());
        int year = stoi(matches[3].str());
        string monthName = getMonthNameFromAPI(lang, monthNum);
        return to_string(day) + " " + monthName + " " + to_string(year);
    }

    // Check for mm-dd-yyyy format
    regex mm_dd_yyyy_regex(R"((\d{1,2})[.\-\/\s]+(\d{1,2})[.\-\/\s]+(\d{4}))");
    if (regex_search(date, matches, mm_dd_yyyy_regex)) {
        int monthNum = stoi(matches[1].str());
        int day = stoi(matches[2].str());
        int year = stoi(matches[3].str());
        string monthName = getMonthNameFromAPI(lang, monthNum);
        return to_string(day) + " " + monthName + " " + to_string(year);
    }

    // If no valid format is found, return an error message
    return "Invalid date format";
}

/*
int main() {
    // Example usage
    string date1 = "2023-10-14";
    string date2 = "14-10-2023";
    string date3 = "October 14, 2023";
    string date4 = "14 de outubro de  2023";
    
    cout << normalizeDate(date1, "pt") << endl;
    cout << normalizeDate(date2, "en") << endl;
    cout << normalizeDate(date3, "en") << endl;
    cout << normalizeDate(date4, "pt") << endl;
    return 0;
}
*/