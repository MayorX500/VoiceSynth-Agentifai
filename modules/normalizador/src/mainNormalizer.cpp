#include <string>
#include "dateNormalization.h"
#include "numNormalizer.h"


using namespace std;

string normalizeText(const string &text, const string &language){
    string dateNormalized = normalizeDate(text, language);
    //string out =normalizeDate(text, language);
    string out = normalizeNumbers(dateNormalized, false, language);


    return out;
}

int main(int argc, char *argv[]){

    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <text> <language>" << endl;
        return 1;  // Return an error code if the input format is wrong
    }

    if(argv[1][0]=='\0'){
        cerr << "Error: Empty String" << endl;
        return 2;
    }

    string input_text = argv[1];

    if(argv[2][0]=='\0'){
        cerr << "Error: Empty language" << endl;
        return 3;
    }

    string language = argv[2];

    string normalizedText = normalizeText(input_text, language);

    // Output the result
    cout << "Original Text: " << input_text << endl;
    cout << "Normalized Text: " << normalizedText << endl;

    return 0;
}