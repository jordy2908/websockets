const express = require('express');
const app = express();


// Clase para representar una sala y su código de invitación
class Room {
  constructor(creator) {
    this.code = this.generateCode();
    this.creator = creator;
    this.users = []
  }

  generateCode() {
    // Generar un código de invitación aleatorio de 6 caracteres
    const characters = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
      code += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return code;
  }

  addUser(socket, user) {
    this.users.push({
      'socketId': socket.id, 
      'user': user, 
      'state': 0
    });
  }

  removeUser(socketId) {
    const index = this.users.findIndex(user => user.socketId === socketId);
    if (index !== -1) {
      this.users.splice(index, 1);
    }
  }
}

// Objeto para almacenar las salas y sus códigos de invitación
const ROOMS = {};

// Objeto para almacenar las conexiones de los jugadores
const players = {};


function createRoom(socket, name) {
  
  const room = new Room(name);

  room.addUser(socket, name);

  socket.join(room.code);

  ROOMS[room.code] = room;

  // console.log(ROOMS)

  socket.emit('event', {
    type: 'create',
    room: ROOMS[room.code]
  });

  socket.emit('event', {
    type: 'join',
    room: ROOMS[room.code]
  });

  console.log(name, 'se ha conectado a la sala', room.code);

  for (let i = 0; i < ROOMS[room.code].users.length; i++) {
    console.log(ROOMS[room.code].users[i])
  }
}

function joinRoom(socket, roomCode, name) {

  let room = ROOMS[roomCode];

  if (room) {
    
    ROOMS[roomCode].addUser(socket, name);

    socket.join(roomCode);

    // socket.emit('test', 'xd');

    socket.emit('event', {
      type: 'join',
      room: ROOMS[roomCode]
    });


    socket.in(roomCode).emit('event', {
      type: 'join',
      room: ROOMS[roomCode]
    });

    console.log(name, 'se ha conectado a la sala', roomCode);

    console.log(ROOMS)

    handlePlayer(socket, name, roomCode);
  } else {
    socket.emit('event', {
      type : 'error',
      msg : 'Código de sala inválido.'
    });
  }
}

// function unregister(socket) {
  
// }

function broadcast(roomCode, message) {
  if (roomCode in ROOMS) {
    const room = ROOMS[roomCode];
    room.users.forEach((user) => {
      user.emit('event', {
        type: 'message',
        msg: message
      });
    });
  }
}

function handlePlayer(socket, name, roomCode) {
  players[name] = { x: 0, y: 0 };

  socket.on('event', (message) => {
    try {
      // Procesar el mensaje recibido del jugador
      const playerPosition = JSON.parse(message);
      // Actualizar las posiciones de los jugadores
      players[name].x = playerPosition.x;
      players[name].y = playerPosition.y;

      // Enviar las nuevas posiciones
      // socket.emit('event', {
      //   type : 'position',
      //   data : JSON.stringify(players)
      // });

      socket.to(roomCode).emit('event', {
        type: 'position',
        players: JSON.stringify(players)
      });

      // imprime en consola las posiciones de los jugadores con el nombre
      console.log(players);
    } catch (error) {
      console.error('Error al procesar el mensaje: ', error);
    }
  });

  // socket.on('disconnect', () => {
  //   console.log('Conexión cerrada');
  //   delete players[name];
  // });
}

function handleSocket(socket) {
  console.log("Se ha conectado un nuevo cliente")

  socket.on('event', (msg) => {

    try {
      console.log('Mensaje recibido:', msg)

      if (msg.type === 'create') {
        createRoom(socket, msg.name);
      } else if (msg.type === 'join') {
          joinRoom(socket, msg.room, msg.name)
      } else {
        socket.emit('error', 'Tipo de mensaje inválido.');
      }

    }

    catch (error) {
      console.error('Error al procesar el mensaje:', error);
    }
  });

  socket.on('disconnect', () => {
    console.log("Se ha desconectado un cliente");
  
    // Recorre todas las salas y elimina al usuario de la sala
    for (let roomCode in ROOMS) {
      const room = ROOMS[roomCode];
      room.removeUser(socket.id);
  
      // Elimina el usuario de ROOMS
      if (room.users.length === 0) {
        delete ROOMS[roomCode];
      }

      socket.in(roomCode).emit('event', {
        type: 'leave',
        room: ROOMS[roomCode]
      });
  
      console.log(`Usuarios en la sala ${roomCode}:`);
      for (let i = 0; i < room.users.length; i++) {
        console.log(room.users[i]);
      }
    }
  });
}

const server = require('http').createServer(app);
const io = require('socket.io')(server, {
  cors: {
    origin: '*',
  }
});


io.on('connection', (socket) => {
  socket.emit('event', {
    type : 'connect',
    msg : 'sorra.'
  });
  handleSocket(socket);
});

// io.on('message', (message) => {
//   console.log('Mensaje recibido:', message);
// });

// inicia el servidor con el metodo cors : *

server.listen(8765, () => {
  console.log('listening on *:8765');
});
