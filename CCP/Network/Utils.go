package Network

import (
	"net"
	"bufio"
	"fmt"
	"log"
	"CCP/Packets"
)

type Client struct {
	Socket    net.Conn
}

func (left_client Client)close_connection() {
	log.Printf("Connection from %v closed.", left_client.Socket.RemoteAddr())

	for client := range client_pool {
		if client == left_client{
			left_client.Socket.Close()
			delete(client_pool, client)
			break
		}
	}

}

func (client Client) Receive_decoded_payload(header []byte) (Packets.Payload,error){

	//Get header
	n, err := client.Socket.Read(header)
	if err != nil || n != HEADER_SIZE {
		log.Print("Header's length received doesn't match HEADER_SIZE: ", ok)
		client.close_connection()
		return nil,ok
	}

	//Parse the header
	parsed_header, err := Packets.Decode_header(header)
	if err != nil {
		log.Print("Problem parsing header: ", err)
		client.close_connection()
		return nil,err
	}

	//Get the payload
	payload_size := int(parsed_header.Payload_length)
	payload, err := client.Rec_all(payload_size)
	if err != nil || len(payload) != payload_size {
		log.Print("Problem getting payload: ", err)
		client.close_connection()
		return nil,err
	}

	decoded_payload, err := Packets.Decode_payload(parsed_header, payload)
	if err != nil {
		log.Print("Problem decoding the payload: ", err)
		client.close_connection()
		return nil,err
	}

	return decoded_payload,nil
}


func (client Client) Rec_all(length int) ([]byte, error) {

	reader := bufio.NewReader(client.Socket)
	buf := make([]byte, length)

	for length > 0 {

		n, err := reader.Read(buf)
		if err != nil || n == 0 {
			return nil, err
		}

		length -= n
	}
	return buf, nil
}


func (client Client) Send_All(data []byte) error {
	length_data := len(data)
	cpt := 0

	for length_data > cpt {
		n, err := client.Socket.Write(data[cpt:])

		if err != nil {
			client.Socket.Close()
			fmt.Println("Connection closed")
			return err
		}
		cpt += n
	}

	return nil
}