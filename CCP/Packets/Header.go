package Packets

import (
	"bytes"
	"encoding/binary"
)

// Size of header: 7 Bytes
type Header struct {
	Command_name   [5]byte
	Payload_length uint16
}

func (header *Header) read_header(packet *bytes.Buffer) error {

	copy(header.Command_name[:], packet.Next(5))
	header.Payload_length = binary.BigEndian.Uint16(packet.Next(2))

	return nil
}

func (header *Header) write_header() []byte {
	var buffer bytes.Buffer

	binary.Write(&buffer, binary.BigEndian, header)
	return buffer.Bytes()
}
