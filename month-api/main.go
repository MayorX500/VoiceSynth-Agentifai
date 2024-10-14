package main

import (
    "net/http"
    "strconv"

    "github.com/gin-gonic/gin"
)

// Data structure to store months in different languages
var months = map[string][]string{
    "en": {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"},
    "es": {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"},
    "fr": {"Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"},
    "pt": {"Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"},
    "de": {"Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"},
}

// Function to handle the months endpoint
func getMonths(c *gin.Context) {
    // Get the language parameter from the query string (e.g., ?lang=en)
    lang := c.DefaultQuery("lang", "en") // Default to English if not provided

    // Check if the language exists in the map
    if monthsForLang, ok := months[lang]; ok {
        // Check if a month number is provided
        monthStr := c.Query("month")
        if monthStr != "" {
            // Convert month string to integer
            monthNumber, err := strconv.Atoi(monthStr)
            if err == nil && monthNumber >= 1 && monthNumber <= 12 {
                // Return the corresponding month name
                c.JSON(http.StatusOK, gin.H{
                    "language": lang,
                    "month":    monthsForLang[monthNumber-1], // monthNumber-1 for zero-based index
                })
                return
            }
            // If the month number is invalid
            c.JSON(http.StatusBadRequest, gin.H{
                "error": "Invalid month number. Must be between 1 and 12.",
            })
            return
        }

        // Return all months for the requested language if no month number is provided
        c.JSON(http.StatusOK, gin.H{
            "language": lang,
            "months":   monthsForLang,
        })
    } else {
        // If the language is not supported, return an error message
        c.JSON(http.StatusBadRequest, gin.H{
            "error": "Language not supported",
        })
    }
}

func main() {
    // Create a new Gin router
    r := gin.Default()

    // Define the endpoint to get months
    r.GET("/months", getMonths)

    // Start the server on port 8080
    r.Run(":8080")
}


// to run:
// go run main.go