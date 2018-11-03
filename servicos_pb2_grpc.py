# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import servicos_pb2 as servicos__pb2


class RequisicaoStub(object):
  """Definição dos serviços oferecidos pelo servidor.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Conectado = channel.unary_unary(
        '/Requisicao/Conectado',
        request_serializer=servicos__pb2.Hello.SerializeToString,
        response_deserializer=servicos__pb2.Resultado.FromString,
        )
    self.Create = channel.unary_unary(
        '/Requisicao/Create',
        request_serializer=servicos__pb2.CreateUpdate.SerializeToString,
        response_deserializer=servicos__pb2.Resultado.FromString,
        )
    self.Read = channel.unary_unary(
        '/Requisicao/Read',
        request_serializer=servicos__pb2.ReadDelete.SerializeToString,
        response_deserializer=servicos__pb2.Resultado.FromString,
        )
    self.Update = channel.unary_unary(
        '/Requisicao/Update',
        request_serializer=servicos__pb2.CreateUpdate.SerializeToString,
        response_deserializer=servicos__pb2.Resultado.FromString,
        )
    self.Delete = channel.unary_unary(
        '/Requisicao/Delete',
        request_serializer=servicos__pb2.ReadDelete.SerializeToString,
        response_deserializer=servicos__pb2.Resultado.FromString,
        )


class RequisicaoServicer(object):
  """Definição dos serviços oferecidos pelo servidor.
  """

  def Conectado(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Create(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Read(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Update(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_RequisicaoServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Conectado': grpc.unary_unary_rpc_method_handler(
          servicer.Conectado,
          request_deserializer=servicos__pb2.Hello.FromString,
          response_serializer=servicos__pb2.Resultado.SerializeToString,
      ),
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=servicos__pb2.CreateUpdate.FromString,
          response_serializer=servicos__pb2.Resultado.SerializeToString,
      ),
      'Read': grpc.unary_unary_rpc_method_handler(
          servicer.Read,
          request_deserializer=servicos__pb2.ReadDelete.FromString,
          response_serializer=servicos__pb2.Resultado.SerializeToString,
      ),
      'Update': grpc.unary_unary_rpc_method_handler(
          servicer.Update,
          request_deserializer=servicos__pb2.CreateUpdate.FromString,
          response_serializer=servicos__pb2.Resultado.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=servicos__pb2.ReadDelete.FromString,
          response_serializer=servicos__pb2.Resultado.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Requisicao', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
