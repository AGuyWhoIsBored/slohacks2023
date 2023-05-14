package main

import (
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"time"

	"github.com/google/uuid"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type classContext struct {
	CurriculumName string   `json:"curriculumName"`
	Classes        []string `json:"classes"`
}

// Friendly list of curriculum names
var curriculumNames = []string{"Astronautics", "Aeronautics", "GRC for Packaging", "GRC for Design Reproduction Technology", "GRC for Communication Managing"}

var commits = map[string]string{
	"Astronautics":                           "astronauticsCurriculum.txt",
	"Aeronautics":                            "aeronauticsCurriculum.txt",
	"GRC for Packaging":                      "grcPackingCurriculum.txt",
	"GRC for Design Reproduction Technology": "grcReproductionCurriculum.txt",
	"GRC for Communication Managing":         "grcManagementCurriculum.txt",
}

func main() {
	router := gin.Default()

	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"https://localhost"},
		AllowMethods:     []string{"POST", "OPTIONS", "GET", "PUT"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		AllowOriginFunc: func(origin string) bool {
			return true
		},
		MaxAge: 12 * time.Hour,
	}))

	router.GET("/curriculum", getCurriculum)
	router.POST("/curriculum", validateClasses)

	router.Run("localhost:8080")
}

// getCurriculum responds with a list of the available curriculums
func getCurriculum(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, curriculumNames)
}

func writeArrToFile(classRequestFileName string, arr []string) {
	f, err := os.Create(classRequestFileName)
	if err != nil {
		fmt.Println(err)
		f.Close()
		return
	}

	for _, class := range arr {
		fmt.Fprintln(f, class)
		if err != nil {
			fmt.Println(err)
			return
		}
	}
	err = f.Close()
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println("file written successfully")
}

// validateClasses checks to see if the classContext fulfills the requirement for a degree
func validateClasses(c *gin.Context) {
	var valRequest classContext

	// Call BindJSON to bind the received JSON to
	// newAlbum.
	if err := c.BindJSON(&valRequest); err != nil {
		return
	}

	fmt.Print("printing val request")
	fmt.Println(valRequest)

	id := uuid.New()
	var classRequestFileName = "classRequest-" + id.String()
	var classRequestResults = "classResults-" + valRequest.CurriculumName + "-" + id.String()

	writeArrToFile(classRequestFileName, valRequest.Classes)

	// python3 PROJECT_DIR\curriculum_validation.py {curriculum txt} {course dabatase} {taken courses list} {outfile}
    cmd := exec.Command("bash", "-c", "python3 ../pythonScripts/curriculum_validation.py" + " " + commits[valRequest.CurriculumName] + " 2020-2021.json ../goBackend/" + classRequestFileName + " ../goBackend/" + classRequestResults)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	fmt.Print(cmd.Run())

	// read output file
	b, err := os.ReadFile(classRequestResults) // just pass the file name
	if err != nil {
		fmt.Print(err)
	}

	res := string(b) // convert content to a 'string'

	os.Remove(classRequestFileName)
	os.Remove(classRequestResults)

	c.IndentedJSON(http.StatusCreated, res)
}
