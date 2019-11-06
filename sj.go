package main

import (
	"fmt"
)

type Game struct {
	InitialState   string
	CurrentState   string
	History        []Move
	MoveTypes      []string
	MoveDirections []string
}

type Move struct {
	Position  int
	Type      string
	Direction string
}

func makeGame(InitialState string) Game {
	g := Game{InitialState, InitialState, []Move{}, []string{"slide", "jump"}, []string{"left", "right"}}
	return g
}

func (g *Game) isValidMove(moveType, moveDirection string) bool {
	// TODO: check if move is valid
	return true
}

func (g *Game) generateMoves() []Move {
	//position int, moveType string, moveDirection string
	var moves []Move
	// TODO: generate moves, append them to slice
	return moves
}

func (g *Game) makeMove(m Move) {

	if m.Type == "slide" {
		//continue
	} else if m.Type == "jump" {

	} else {
		panic(fmt.Printf("bad move given %v", m))
	}

	g.History = append(g.History)
}

func (g *Game) display() {
	fmt.Println("game:")
	fmt.Printf("InitialState: %v\n", g.InitialState)
	fmt.Printf("CurrentState: %v\n", g.CurrentState)
	fmt.Printf("History: %v\n", g.History)
}

func main() {
	g := makeGame("h_t")
	g.display()
	g.History = append(g.History, g.CurrentState)
	g.display()
}
