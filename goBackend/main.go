package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type classContext struct {
	curriculumName string   `json:"curriculumName"`
	classes        []string `json:"classes"`
}

// Friendly list of curriculum names
var curriculumNames = []string{"Astronautics", "Aeronautics", "GRC for Packaging", "GRC for Design Reproduction Technology", "GRC for Communication Managing"}

func main() {
	router := gin.Default()
	router.GET("/curriculum", getCurriculum)
	router.POST("/curriculum", validateClasses)

	router.Run("localhost:8080")
}

// getCurriculum responds with a list of the available curriculums
func getCurriculum(c *gin.Context) {
	c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
	c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
	c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
	c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")
	c.IndentedJSON(http.StatusOK, curriculumNames)
}

// validateClasses checks to see if the classContext fulfills the requirement for a degree
func validateClasses(c *gin.Context) {
	var valRequest classContext

	c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
	c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
	c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
	c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")

	// Call BindJSON to bind the received JSON to
	// newAlbum.
	if err := c.BindJSON(&valRequest); err != nil {
		return
	}

	// add processing logic here

	c.IndentedJSON(http.StatusCreated, valRequest)
}
