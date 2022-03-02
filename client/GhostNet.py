from client import GhostClient

if __name__ == '__main__':
  print('Inicializando o GhostNet Client...')

  client = GhostClient('localhost', 50005)
  client.start()
  client.join()


