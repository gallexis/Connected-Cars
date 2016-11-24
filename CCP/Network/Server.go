package Network

import (
	"CCP/Packets"
	"CCP/Packets/Payloads"
	"fmt"
	"log"
	"net"
)

var client_pool = make(map[Client]net.Addr)
var HEADER_SIZE int = 7

func Broadcast(emiter Client, message []byte){

	for sock,ip := range client_pool {
		if sock != emiter{
			sock.Socket.Write(message)
			log.Println("Broadcasted from "+emiter.Socket.RemoteAddr().String()+", to :"+ip.String())
		}
	}

}

func Server_handle_connection(client Client) {
	log.Printf("Client %v connected.", client.Socket.RemoteAddr())

	header := make([]byte, HEADER_SIZE)

	for {
		decoded_payload,err := client.Receive_decoded_payload(header)
		if err != nil{
			log.Print("Error Receive_decoded_payload: ",err)
			break
		}
		binary_payload := Packets.Create_packet(decoded_payload)

		//Broadcast the message to all the other nodes
		//Have to re-encode the decoded packet in order to breoadcast it
		go Broadcast(client,append(header,binary_payload...))

		//The server can have a global view of the transmitted messages
		//among the nodes

		//Decode the payload & do whatever the server wants (logging..)
		switch payload := decoded_payload.(type) {
		case Payloads.Alert:
			fmt.Println("Alert message :D")
			fmt.Println(string(payload.Description))

		default:
			fmt.Print(":/")

		}
	}
}


func Start_server() {
	ln, err := net.Listen("tcp", ":6000")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Server up and listening on port 6000")

	for {
		sock, err := ln.Accept()

		if err != nil {
			log.Print("Error incoming connection: ")
			log.Println(err)
			sock.Close()
			continue
		}

		client := Client{Socket:sock}
		client_pool[client] = sock.RemoteAddr()
		go Server_handle_connection(client)
	}
}
