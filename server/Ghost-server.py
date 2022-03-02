from server import GhostServer

if __name__ == '__main__':

  print('Inicializando o GhostNet Server...')

  server = GhostServer('localhost', 50005)
  server.start()

