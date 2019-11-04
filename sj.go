package main

import (
	"fmt"
)

type Game struct {
	InitialState string
	CurrentState string
	History      []string
}

func makeGame(InitialState string) Game {
	g := Game{InitialState, InitialState, []string{}}
	return g
}

func (g *Game) isValid() bool {

	return true
}

func (g *Game) makeMove(position int, moveType string, moveDirection string) {
	if moveType == "slide" {

	}
}

func (g *Game) display() {
	fmt.Println("game:")
	fmt.Printf("InitialState: %v\n", g.InitialState)
	fmt.Printf("History: %v\n", g.History)
}

func main() {
	g := makeGame("h_t")
	g.display()
}
