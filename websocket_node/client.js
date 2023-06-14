const io = require('socket.io-client');
const socket = io('http://192.168.100.165:8765');

socket.on('connect', () => {
    console.log('Conectado al servidor');
    });

socket.emit('message', 'join,N7SPP2', (resp) => {
    console.log('Respuesta del servidor:', resp);
  });

socket.emit('sendUsername', 'dani', (resp) => {
    console.log('Respuesta del servidor:', resp);
    });

socket.on('disconnect', () => {
  console.log('Desconectado del servidor');
});

socket.on('message', (message) => {
  console.log('Mensaje recibido:', message);
});
