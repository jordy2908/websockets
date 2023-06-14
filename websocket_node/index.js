const http = require('http');
const { Server } = require('socket.io');

// Clase para representar una sala y su código de invitación
class Room {
  constructor(creator) {
    this.code = this.generateCode();
    this.creator = creator;
    this.users = new Set();
  }

  generateCode() {
    // Generar un código de invitación aleatorio de 6 caracteres
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
      code += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return code;
  }

  addUser(user) {
    this.users.add(user);
  }

  removeUser(user) {
    this.users.delete(user);
  }

  isEmpty() {
    return this.users.size === 0;
  }
}

// Objeto para almacenar las salas y sus códigos de invitación
const ROOMS = {};

// Objeto para almacenar las conexiones de los jugadores
const players = {};

function createRoom(socket, name) {
  const room = new Room(name);
  ROOMS[room.code] = room;
  socket.emit('create', room.code);

  // Ingresa directamente a la sala con el nombre de usuario que ingresó sin pedir el nombre porque el nombre ya se lo pasamos al crear la sala
  room.addUser(socket);

  socket.emit('join', `${room.code}.`);

  console.log(name, 'se ha conectado a la sala', room.code);

  handlePlayer(socket, name);
}

function joinRoom(socket, roomCode) {
  // Verificar si el código de invitación es válido y si la sala existe
  if (roomCode in ROOMS) {
    const room = ROOMS[roomCode];

    // Solicitar al usuario que ingrese su nombre de usuario
    socket.emit('requestUsername');
    socket.on('sendUsername', (username) => {
      // Agregar el objeto socket a la sala en lugar del nombre de usuario
      room.addUser(socket);
      socket.emit('join', roomCode);

      // Enviar un mensaje de bienvenida a todos los usuarios de la sala
      room.users.forEach((user) => {
        if (user !== socket) {
          user.emit('userJoined', username);
        }
      });

      handlePlayer(socket, username);
      
    });
  } else {
    socket.emit('error', 'Código de invitación inválido.');
    socket.on('sendRoomCode', (newRoomCode) => {
      joinRoom(socket, newRoomCode);
    });
  }
}

function unregister(socket) {
  for (const [roomCode, room] of Object.entries(ROOMS)) {
    if (room.users.has(socket)) {
      room.removeUser(socket);
      if (room.isEmpty()) {
        delete ROOMS[roomCode];
      }
    }
  }
}

function broadcast(roomCode, message) {
  if (roomCode in ROOMS) {
    const room = ROOMS[roomCode];
    room.users.forEach((user) => {
      user.emit('message', message);
    });
  }
}

function handlePlayer(socket, name) {
  players[name] = { x: 0, y: 0 };

  console.log(name, 'se ha conectado')

  socket.on('message', (message) => {
    try {
      // Procesar el mensaje recibido del jugador
      const playerPosition = JSON.parse(message);
      // Actualizar las posiciones de los jugadores
      players[name].x = playerPosition.x;
      players[name].y = playerPosition.y;

      // Enviar las nuevas posiciones
      socket.emit('message', JSON.stringify(players));
      // imprime en consola las posiciones de los jugadores con el nombre
      console.log(players);
    } catch (error) {
      console.error('Error al procesar el mensaje:', error);
    }
  });

  socket.on('disconnect', () => {
    console.log('Conexión cerrada');
    delete players[name];
  });
}

function handleSocket(socket) {
  socket.on('message', (message) => {
    const [command, data] = message.split(',');
    if (command === 'create') {
      createRoom(socket, data);
    } else if (command === 'join') {
        // console.log('join, ', data);
      joinRoom(socket, data);
    }
  });

  socket.on('disconnect', () => {
    unregister(socket);
  });
}

const server = http.createServer();
const io = new Server(server);

io.on('connection', (socket) => {
  handleSocket(socket);
});

server.listen(8765, '0.0.0.0', () => {
  console.log('Servidor escuchando en el puerto 8765');
});
