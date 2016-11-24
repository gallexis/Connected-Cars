package Packets

type Payload interface {
	Get_command_name() string
	Forge() []byte
}
