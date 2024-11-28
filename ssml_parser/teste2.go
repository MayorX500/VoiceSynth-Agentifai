package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"regexp"
	"strings"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Wrong usage: go run program.go \"file\" \"language\"")
		return
	}

	filePath := os.Args[1]
	lang := os.Args[2] // Language parameter, although currently unused in this version.

	content, err := ioutil.ReadFile(filePath)
	if err != nil {
		fmt.Printf("Error: The file %s was not found.\n", filePath)
		return
	}

	ssmlText := string(content)
	fmt.Println("Original Text:\n", ssmlText)

	parsedText := parseSSML(ssmlText, lang)
	fmt.Println("\nParsed Text:\n", parsedText)
}

// parseSSML parses SSML text and replaces certain tags with text.
func parseSSML(ssmlText, lang string) string {
	replacements := map[string]interface{}{
		`<speak>`:                      "",
		`</speak>`:                     "",
		`<break time="(\d+)(ms|s)"\/>`: func(m []string) string { return fmt.Sprintf("[pause for %s second(s)]", m[1]) },
		`<say-as interpret-as="characters">(.*?)</say-as>`: func(m []string) string { return strings.Join(strings.Split(m[1], ""), " ") },
		`<say-as interpret-as="cardinal">(.*?)</say-as>`:   func(m []string) string { return numToWords(m[1], "cardinal", lang) },
		`<say-as interpret-as="ordinal">(.*?)</say-as>`:    func(m []string) string { return numToWords(m[1], "ordinal", lang) },
		`<say-as interpret-as="currency">(.*?)</say-as>`:   func(m []string) string { return numToWords(m[1], "currency", lang) },
		`<sub alias="(.*?)">(.*?)</sub>`:                   func(m []string) string { return m[1] },
		`<audio src="(.*?)">(.*?)</audio>`:                 "[audio file plays]",
		`<p>`:                                              "", `</p>`: "", `<s>`: "", `</s>`: "",
	}
	for pattern, replacement := range replacements {
		re := regexp.MustCompile(pattern)
		if replFunc, ok := replacement.(func([]string) string); ok {
			ssmlText = re.ReplaceAllStringFunc(ssmlText, func(match string) string {
				return replFunc(re.FindStringSubmatch(match))
			})
		} else if replStr, ok := replacement.(string); ok {
			ssmlText = re.ReplaceAllString(ssmlText, replStr)
		}
	}

	// Remove any remaining tags
	re := regexp.MustCompile(`<.*?>`)
	ssmlText = re.ReplaceAllString(ssmlText, "")

	return strings.TrimSpace(ssmlText)
}

// numToWords converts a number to words based on the given type (cardinal, ordinal, etc.).
func numToWords(numStr, numType, lang string) string {
	cmd := exec.Command("python3", "convert_numbers.py", numStr, lang, numType)
	out, _ := cmd.Output()
	return strings.TrimSpace(string(out))
}

//eu amo a margarida
//A MARGARIDA E O AMOR DA MINHA VIDA
