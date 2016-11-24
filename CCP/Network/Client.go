package Network

import (
	"fmt"
	"net"
	"CCP/Packets/Payloads"
	"log"
)

func NewConnection(hostName string, port string) (Client, error) {
	connection := Client{Socket: nil}

	sock, err := net.Dial("tcp", hostName+":"+port)
	if err != nil {
		log.Println(err)
		return connection, err
	}

	connection.Socket = sock

	fmt.Printf("Connection established between %s and localhost.\n", hostName)
	fmt.Printf("Remote Address : %s \n", sock.RemoteAddr().String())
	fmt.Printf("Local Address : %s \n", sock.LocalAddr().String())

	return connection, nil
}

func Client_handle_connection(client Client) {
	header := make([]byte, HEADER_SIZE)

	for{
		decoded_payload,err := client.Receive_decoded_payload(header)
		if err != nil{
			break
		}
		//Decode the payload & do whatever the server wants
		switch payload := decoded_payload.(type) {
		case Payloads.Alert:
			fmt.Println("Alert message :D")
			fmt.Println(string(payload.Description))

		default:
			fmt.Print(":/")

		}
	}
}
